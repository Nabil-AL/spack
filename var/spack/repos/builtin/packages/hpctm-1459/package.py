##############################################################################
# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Hpctm1459(CMakePackage):
    """HPCTM1459"""

    homepage = "https://bbpteam.epfl.ch/project/issues/browse/HPCTM-1459"
    url      = "git@bbpgitlab.epfl.ch:hpc/user/hpctm-1459.git"
    git      = "git@bbpgitlab.epfl.ch:hpc/user/hpctm-1459.git"

    version('develop', branch='main', submodules=False)
    version('0.1', commit='efcee5', submodules=False)

    depends_on('cmake', type='build')

    def cmake_args(self):
        return [
            '-DINTERNAL_PACKAGES:BOOL=OFF'
        ]
