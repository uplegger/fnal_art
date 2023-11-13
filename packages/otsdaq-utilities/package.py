# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class OtsdaqUtilities(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/otsdaq_utilities/archive/refs/tags/v2_06_08.tar.gz"
    git = "https://github.com/art-daq/otsdaq_utilities.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_07_00", sha256="3aa8db47f2cd3a870eadbf8b189c6e96b61be5b54ee06ffd28f1978b5d32df32")
    version("v2_06_11", sha256="1f6dde48c4c5771fce3dfa8ee2d274ebe4191adf775d05130964b0c4d79a82a6")
    version("v2_06_10", sha256="4e68e399d765fb729f1de90cb4cdd13c4fd150fc4e2ad0e7a1c5d09d4a7900b5")
    version("v2_06_09", sha256="852b4e051fe418786c3c161a548a8eb46d45c59578c9954f2ce68c6a62e2fc47")
    version("v2_06_08", sha256="cb024d6b7d98b343b74b9837d1a1161cc9d0bd92f027fffe56ae6d156e952a64")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq_utilities/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", conditional("20",when="@v2_06_10:")),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")

    depends_on("otsdaq")

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find WebGUI Data
        env.set("OTSDAQ_UTILITIES_DIR", prefix)
        # Ensure we can find libraries
        env.set("OTSDAQ_UTILITIES_LIB", prefix.lib)

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find WebGUI Data
        env.set("OTSDAQ_UTILITIES_DIR", prefix)
        # Ensure we can find libraries
        env.set("OTSDAQ_UTILITIES_LIB", prefix.lib)

