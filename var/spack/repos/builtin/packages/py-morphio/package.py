# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphio(PythonPackage):
    """Python library for reading / writing morphology files"""

    homepage = "https://github.com/BlueBrain/MorphIO/"
    git      = "https://github.com/BlueBrain/MorphIO.git"

    version('develop', branch='master', submodules=True, get_full_repo=True)
    version('unifurcation', branch='unifurcation', submodules=True, get_full_repo=True)
    version('2.3.10', tag='v2.3.10', submodules=True, get_full_repo=True)
    version('2.3.4', tag='v2.3.4', submodules=True, get_full_repo=True)
    version('2.2.1', tag='v2.2.1', submodules=True, get_full_repo=True)
    version('2.1.2', tag='v2.1.2', submodules=True, get_full_repo=True)
    version('2.0.8', tag='v2.0.8', submodules=True, get_full_repo=True)

    variant('use_double', default=False, description='Use doubles instead of float')
    depends_on('py-setuptools', type='build')

    depends_on('cmake@3.2:', type='build')
    depends_on('py-numpy', type='run')
    depends_on('hdf5~mpi', type=('build', 'run'))

    phases = ['build_ext', 'install']

    def build_ext_args(self, spec, prefix):
        """Arguments to pass to build_ext."""
        if  self.spec.satisfies('+use_double'):
            return ['--cmake-defs=MORPHIO_USE_DOUBLE=ON']
        return []
