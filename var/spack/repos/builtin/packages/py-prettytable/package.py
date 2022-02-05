# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPrettytable(PythonPackage):
    """PrettyTable is a simple Python library designed to make
    it quick and easy to represent tabular data in visually
    appealing ASCII tables.
    """

    homepage = "https://github.com/jazzband/prettytable"
    pypi = "prettytable/prettytable-2.2.1.tar.gz"

    version('2.2.1', sha256='6d465005573a5c058d4ca343449a5b28c21252b86afcdfa168cdc6a440f0b24c')
    version('0.7.2', sha256='2d5460dc9db74a32bcc8f9f67de68b2c4f4d2f01fa3bd518764c69156d9cacd9')

    depends_on('python@3.6:', when='@2.0.0:', type=('build', 'run'))
    depends_on("py-setuptools", type='build')
    depends_on('py-importlib-metadata', when='@2.2.1:^python@:3.8', type=('build', 'run'))
    depends_on('py-wcwidth', when='@1.0.0:', type=('build', 'run'))
