# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDocsInternalUpload(PythonPackage):
    """A Python package and command line tool for uploading your project
    documentation to the Blue Brain Project internal documentation git
    repository."""

    homepage = "https://bbpgitlab.epfl.ch/nse/documentation/docs-internal-upload"
    git      = "git@bbpgitlab.epfl.ch:nse/documentation/docs-internal-upload.git"

    version('develop')
    version('0.1.0', commit='66d36a4537e20b7522f2b912319f472a0e15a084')

    depends_on('py-setuptools', type='build')
    depends_on('py-click', type='run')
    depends_on('py-packaging', type='run')
