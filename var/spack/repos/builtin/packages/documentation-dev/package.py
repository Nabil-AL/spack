# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DocumentationDev(BundlePackage):
    """Meta package to bundle packages for documentation building"""

    homepage = "http://www.dummy.org/"
    url      = "https://www.dummy.org/source/dummy-0.2.zip"

    version('0.1')

    depends_on('python', type=('build', 'run'))
    depends_on('py-docs-internal-upload', type=('build', 'run'))
    depends_on('py-sphinx-bluebrain-theme', type=('build', 'run'))

    def setup_run_environment(self, env):
        for dep in self.spec.dependencies(deptype='run'):
            env.prepend_path('PATH', dep.prefix.bin)
