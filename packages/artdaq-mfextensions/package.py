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

class ArtdaqMfextensions(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_mfextensions/archive/refs/tags/v1_08_02.tar.gz"
    git = "https://github.com/art-daq/artdaq_mfextensions.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v1_08_06", sha256="3689545eb4126a5a3501703d3f91e9f4725366e8fd7bbfa4e0999e9183dc8884")
    version("v1_08_05", sha256="a92d230f6555fcfc565e6907d4ef02d0f7f1491db90605e0f49485dec7c63e6e")
    version("v1_08_04", sha256="2f6cdcd0dd083d91761df06d203487613723d770051e17b967f499e4348de7c9")
    version("v1_08_03", sha256="c83c8c3c0bb525ae504b5efee910d5a2e7c0278ddc46b04461c76425e652de62")
    version("v1_08_02", sha256="d03b4261491bc879a34908c70f7f49cd64624ec889bfb8f486f7ce9fd1bd7f6b")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_mfextensions/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", conditional("20",when="@v1_08_04:")),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")
    depends_on("qt@5.15:")

    depends_on("trace+mf")

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
    
