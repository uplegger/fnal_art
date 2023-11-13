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

class ArtdaqEpicsPlugin(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_epics_plugin/archive/refs/tags/v1_05_02.tar.gz"
    git = "https://github.com/art-daq/artdaq_epics_plugin.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v1_05_06", sha256="b0e0c203199eb3a826a3560345a8e7f9b5ae2f81941caf7c6fe3730dad0b9d27")
    version("v1_05_04", sha256="b59d8022b00935e4d4fcfcc2a853113c7551473b6f7bdd19ade8e42363062ab8")
    version("v1_05_03", sha256="68937458d87d53ac20607b9e62ac13616c143f3f074675b047897a0b10cf20f0")
    version("v1_05_02", sha256="8a8d12f29a357c2426c16c3aef1a745b6bf3308ede38aae2300584eff582a3cf")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_epics_plugin/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", conditional("20",when="@v1_05_04:")),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")
    depends_on("epics-base")

    depends_on("artdaq-utilities")

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


