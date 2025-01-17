# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Brion(CMakePackage):
    """Blue Brain C++ File IO Library"""

    homepage = "https://github.com/BlueBrain/Brion"
    git = "https://github.com/BlueBrain/Brion.git"
    generator = "Ninja"

    submodules = True

    version("develop", branch="master")
    version("3.3.9", tag="3.3.9", submodules=False)

    variant("python", default=False, description="Build Python wrapping")
    variant("doc", default=False, description="Build documentation")

    depends_on("cmake@3.1:", type="build")
    depends_on("ninja", type="build")
    depends_on("doxygen", type="build")

    depends_on("python@3.4:", type=("build", "run"), when="+python")
    depends_on("py-numpy", type=("build", "run", "test"), when="+python")

    depends_on(
        "boost +date_time+filesystem+iostreams+program_options+regex+shared+system+test",
        when="~python",
    )
    depends_on(
        "boost +date_time+filesystem+iostreams+program_options+regex+shared+system+test+python",
        when="+python",
    )

    depends_on("libsonata")
    depends_on("morphio")

    # TODO: bzip2 is a dependency of boost. Needed here because of linking
    # issue (libboost_iostreams.so.1.68.0 not finding libbz2.so)
    depends_on("bzip2")
    depends_on("highfive +boost")
    depends_on("mvdtool")
    depends_on("glm@:0.9.9.5")

    extends("python", when="+python")

    patch(
        "https://patch-diff.githubusercontent.com/raw/BlueBrain/Brion/pull/334.patch?full_index=1",
        sha256="a1100b4581d424e3717bac1f5bf5682bd04b9e778213fb51014276b5b0d19bf9",
        when="@3.3.4 ^python@3.9:",
    )

    def patch(self):
        filter_file(
            r"-Werror",
            "-Werror -Wno-error=deprecated-copy -Wno-error=range-loop-construct "
            "-Wno-error=unused-function",
            "CMake/CompileOptions.cmake",
        )

    def cmake_args(self):
        args = [
            "-DBRION_SKIP_LIBSONATA_SUBMODULE=ON",
            "-DDISABLE_SUBPROJECTS=0N",
            "-DBRION_REQUIRE_PYTHON=%s" % ("ON" if "+python" in self.spec else "OFF"),
        ]
        return args

    def setup_run_environment(self, env):
        if self.spec.satisfies("+python"):
            site_dir = self._get_site_dir()
            for target in (self.prefix.lib, self.prefix.lib64):
                pathname = os.path.join(target, *site_dir)
                if os.path.isdir(pathname):
                    env.prepend_path("PYTHONPATH", pathname)

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            ninja()
            if "+doc" in self.spec:
                ninja("doxygen", "doxycopy")

    @when("+python")
    @run_after("install")
    def test(self):
        site_dir = self._get_site_dir()
        for target in (self.prefix.lib, self.prefix.lib64):
            pathname = os.path.join(target, *site_dir)
            if os.path.isdir(pathname):
                with working_dir(pathname):
                    python("-c", "import brion; print(brion)")

    def _get_site_dir(self):
        return self.spec["python"].package.platlib
