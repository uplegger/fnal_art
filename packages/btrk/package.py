# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Btrk(SConsPackage):
    """Mu2e experiment: Refactoring BField Interface package
    """

    homepage = "https://github.com/KFTrack/Btrk#readme"
    url = "https://github.com/KFTrack/BTrk/archive/refs/tags/v1_02_43.tar.gz"

    # maintainers("github_user1", "github_user2")

    #version("v1_02_43", sha256="55eb787f156f380c80240b9f91d99963db47f015988d4cbdd3ee09e95af7759e")
    version("v1_02_41", sha256="4b233ebe252f82a1f4d857c04b44c6a62a49049ed69172cb347a1b180b50770c")

    def url_for_version(self, version):
        url = "https://github.com/KFTrack/BTrk/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    depends_on("root")
    depends_on("clhep")

    def build_args(self, spec, prefix):
        args = []
        return args

    def setup_build_environment(self, env):
        env.set("PYTHONPATH", "%s/python" % self.stage.source_dir)
