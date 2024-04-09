# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larbatch(Package):
    """package for batch job submission featuring project.py"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larbatch-web-client/wiki"
    url = "https://github.com/LArSoft/larbatch/archive/refs/tags/v01_51_15.tar.gz"

    version("01.51.15", sha256="adc956e621f36c7fbf37f85c737e793d8fc8e58ad44ec3077ea80830f1b7ad25")


    depends_on("sam-web-client", type=("run"))
    depends_on("python", type=("run"))

    def url_for_version(self, version):
        urlf = "https://github.com/LArSoft/larbatch/archive/refs/tags/v%s.tar.gz"
        return urlf % version.underscored

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PYTHONPATH", self.prefix.bin)
        run_env.prepend_path("PYTHONPATH", self.prefix + "/python")
