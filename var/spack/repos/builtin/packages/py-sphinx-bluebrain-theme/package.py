# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxBluebrainTheme(PythonPackage):
    """Sphinx Limestone Theme"""

    homepage = "https://github.com/BlueBrain/sphinx-bluebrain-theme"
    git = "https://github.com/BlueBrain/sphinx-bluebrain-theme.git"

    version('develop', submodules=True)
    version('0.2.4', tag='v0.2.4', submodules=True)

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-sphinx@2:', type='run')

    @run_before('build')
    def generate(self):
        python = self.spec['python'].command
        python('translate_templates.py')
