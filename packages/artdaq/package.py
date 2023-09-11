# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class Artdaq(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq/archive/refs/tags/v3_12_04.tar.gz"
    git = "https://github.com/art-daq/artdaq.git"


    version("develop", branch="develop", get_full_repo=True)
    version("v3_12_05", sha256="871a2386d324059de13b94819ec11e731598a1ac124bb2e8c2b29ed7f9af9309")
    version("v3_12_04", sha256="0221d41878d3e99b7b40ff46e3d4a9542f07bb81bb21d4cfbb223e06f2a57502")
    version("v3_12_03", sha256="2300fd0c78d33b411cfd05b552242e1a816e457e6d13880c35e7167df77b114f")
    version("v3_12_02", sha256="98baad840c49be9b16d8dc819a708505fa8601fcb42844c17c1013f9d75b728e")
    version("v3_12_01", sha256="558945c67974b3bb6a1b8d8a28089f2f33d13183f21d49c0e916204896453c53")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", conditional("20",when="@v3_12_04:")),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
    )

    depends_on("art-root-io")
    
    depends_on("cetmodules", type="build")
    depends_on("xmlrpc-c+curl")
    depends_on("swig", type="build")
    depends_on("node-js", type="build")

    depends_on("artdaq-core")
    depends_on("artdaq-utilities")
    depends_on("artdaq-mfextensions")

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")
