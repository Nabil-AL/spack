# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyNeurodamus(PythonPackage):
    """The BBP simulation control suite, Python API"""

    homepage = "https://bbpteam.epfl.ch/project/spaces/display/BGLIB/Neurodamus"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/sim/neurodamus-py.git"

    version("develop", branch="main", submodules=True)
    version("2.13.2", tag="2.13.2", submodules=True)
    version("2.13.1", tag="2.13.1", submodules=True)
    version("2.13.0", tag="2.13.0", submodules=True)
    version("2.12.11", tag="2.12.11", submodules=True)
    version("2.12.10", tag="2.12.10", submodules=True)
    version("2.12.9", tag="2.12.9", submodules=True)
    version("2.12.8", tag="2.12.8", submodules=True)
    version("2.12.7", tag="2.12.7", submodules=True)
    version("2.12.6", tag="2.12.6", submodules=True)
    version("2.12.5", tag="2.12.5", submodules=True)
    version("2.12.4", tag="2.12.4", submodules=True)
    version("2.12.3", tag="2.12.3", submodules=True)
    version("2.12.2", tag="2.12.2", submodules=True)
    version("2.12.1", tag="2.12.1", submodules=True)
    version("2.12.0", tag="2.12.0", submodules=True)
    version("2.11.3", tag="2.11.3", submodules=True)
    version("2.11.2", tag="2.11.2", submodules=True)
    version("2.11.1", tag="2.11.1", submodules=True)
    version("2.10.3", tag="2.10.3", submodules=True)
    version("2.10.2", tag="2.10.2", submodules=True)
    version("2.10.1", tag="2.10.1", submodules=True)
    version("2.10.0", tag="2.10.0", submodules=True)
    version("2.9.0", tag="2.9.0", submodules=True)

    # Note: we depend on Neurodamus but let the user decide which one.
    # Note: avoid Neuron/py-mvdtool dependency due to Intel-GCC conflicts.
    depends_on("python@3.4:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numpy@:1.22", type=("build", "run"))
    depends_on("py-docopt", type=("build", "run"))
    depends_on("py-libsonata", type=("build", "run"))
    depends_on("py-morphio", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"), when="@2.12.1:")

    @run_after("install")
    def install_files(self):
        from llnl.util.filesystem import copy

        mkdirp(self.prefix.share)
        for script in ("init.py", "_debug.py"):
            copy(script, self.prefix.share)
        install_tree("core/hoc", self.prefix.lib.hoc)
        install_tree("core/mod", self.prefix.lib.mod)
        install_tree("core/python", self.prefix.lib.python)

    def setup_run_environment(self, env):
        PythonPackage.setup_run_environment(self, env)
        env.set("NEURODAMUS_PYTHON", self.prefix.share)

    LATEST_STABLE = "develop"  # Use for neurodamus-models (updated below)


# Update LATEST_STABLE
# Note: Directives are lazyly executed. The `versions` attr is only avail now
_all_versions = sorted(PyNeurodamus.versions)
_max_version = None
if _all_versions:
    _max_version = _all_versions[-1]
    if _max_version.isdevelop() and len(_all_versions) > 1:
        _max_version = _all_versions[-2]
    PyNeurodamus.LATEST_STABLE = _max_version.string
