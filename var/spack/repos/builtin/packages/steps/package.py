# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Steps(CMakePackage):
    """STochastic Engine for Pathway Simulation"""

    homepage = "https://groups.oist.jp/cnu/software"
    git      = "git@bbpgitlab.epfl.ch:hpc/HBP_STEPS.git"

    version("develop", branch="master", submodules=True)
    version("3.6.0", submodules=True)
    version("3.5.0b",  commit="b2be5fe", submodules=True)
    version("3.4.1", submodules=True)
    version("3.3.0", submodules=True)
    version("3.2.0", submodules=True)

    variant("codechecks", default=False,
            description="Perform additional code checks like "
                        "code formatting or static analysis")
    variant("native", default=True, description="Generate non-portable arch-specific code")
    variant("lapack", default=False, description="Use new BDSystem/Lapack code for E-Field solver")
    variant("distmesh", default=False, description="Add solvers based on distributed mesh")
    variant("petsc", default=False, description="Use PETSc library for parallel E-Field solver")
    variant("mpi", default=True, description="Use MPI for parallel solvers")
    variant("coverage", default=False, description="Enable code coverage")
    variant("bundle", default=False, description="Use bundled libraries")
    variant("stochtests", default=True, description="Add stochastic tests to ctests")

    depends_on("boost")
    depends_on("blas")
    depends_on("lapack", when="+lapack")
    depends_on("lcov", when="+coverage", type="build")
    depends_on("metis+int64", when="@3.6.1:")
    depends_on("eigen", when="@3.6.1:")
    depends_on("mpi", when="+mpi")
    depends_on("petsc~debug+int64+mpi", when="+petsc+mpi")
    depends_on("petsc~debug+int64~mpi", when="+petsc~mpi")
    depends_on("py-cmake-format", type="build", when="+codechecks")
    depends_on("py-cython")
    depends_on("py-gcovr", when="+coverage", type="build")
    depends_on("py-matplotlib", type=("build", "test"))
    depends_on("py-mpi4py", when="+distmesh")
    depends_on("py-nose", type=("build", "test"))
    depends_on("py-numpy", type=("build", "test"))
    depends_on("py-scipy", type=("build", "test"))
    depends_on("py-unittest2", type=("build", "test"))
    depends_on("python")
    depends_on('py-pre-commit', type='build', when='+codechecks')
    depends_on('py-pyyaml', type='build', when='+codechecks')
    depends_on("omega-h+gmsh+mpi", when="~bundle+distmesh")
    depends_on("gmsh", when="+distmesh")
    depends_on("easyloggingpp", when="~bundle")
    depends_on("random123", when="~bundle")
    depends_on("sundials@:2.99.99+int64", when="~bundle")
    conflicts("+distmesh~mpi",
              msg="steps+distmesh requires +mpi")

    patch('for_aarch64.patch', when='target=aarch64:')

    def cmake_args(self):
        args = []
        spec = self.spec

        use_bundle = "ON" if "+bundle" in spec else "OFF"
        bundles = [
            "EASYLOGGINGPP",
            "OMEGA_H",
            "RANDOM123",
            "SUNDIALS",
            "SUPERLU_DIST"
        ]
        args.extend("-DUSE_BUNDLE_{0}:BOOL={1}".format(bundle, use_bundle)
                    for bundle in bundles)

        if "+native" in spec:
            args.append("-DTARGET_NATIVE_ARCH:BOOL=True")
        else:
            args.append("-DTARGET_NATIVE_ARCH:BOOL=False")

        if "+lapack" in spec:
            args.append("-DUSE_BDSYSTEM_LAPACK:BOOL=True")
        else:
            args.append("-DUSE_BDSYSTEM_LAPACK:BOOL=False")

        if "+petsc" in spec:
            args.append("-DUSE_PETSC:BOOL=True")
        else:
            args.append("-DUSE_PETSC:BOOL=False")

        if "+mpi" in spec:
            args.append("-DUSE_MPI:BOOL=True")
        else:
            args.append("-DUSE_MPI:BOOL=False")

        if "+coverage" in spec:
            args.append("-DENABLE_CODECOVERAGE:BOOL=True")

        if "+distmesh" in spec:
            args.append("-DUSE_DISTRIBUTED_MESH:BOOL=True")
        else:
            args.append("-DUSE_DISTRIBUTED_MESH:BOOL=False")

        if "+stochtest" in spec:
            args.append("-DBUILD_STOCHASTIC_TESTS:BOOL=True")
        else:
            args.append("-DBUILD_STOCHASTIC_TESTS:BOOL=False")

        if "+codechecks" in spec:
            args.append("-DENABLE_ERROR_ON_WARNING:BOOL=TRUE")
        else:
            args.append("-DENABLE_ERROR_ON_WARNING:BOOL=FALSE")

        args.append('-DBLAS_LIBRARIES=' + spec['blas'].libs.joined(";"))
        args.append('-DPYTHON_EXECUTABLE='
                    + spec['python'].prefix.bin.python
                    + str(spec['python'].version.up_to(1)))
        return args

    @property
    def build_targets(self):
        targets = []
        if "+coverage" in self.spec:
            if self.compiler.name != "gcc":
                raise ValueError(
                    "Package " + self.name +
                    " build with coverage enabled requires GCC to build"
                )
            targets = [
                "CTEST_OUTPUT_ON_FAILURE=1",
                "all",  # build
                "coverage_init",  # initialize coverage counters
                "test",  # run tests suite
                "coverage"  # collect coverage counters and build reports
            ]
        return targets

    def setup_run_environment(self, env):
        # This recipe exposes a Python package from a C++ CMake project.
        # This hook is required to reproduce what Spack PythonPackage does.
        env.prepend_path('PYTHONPATH', self.prefix)
