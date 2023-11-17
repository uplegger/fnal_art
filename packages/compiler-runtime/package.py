# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
import os


class CompilerRuntime(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/FNALssi/"
    url = "file:///dev/null"

    maintainers("marcmengel")

    version("see_compiler", sha256="364fd6d448b2398150a4d8aa3a3d3564a373aeb7dfb3a477f56685a356c88159")

    def url_for_version(self, version):

        if not os.access("/tmp/empty.tar",os.R_OK):
            tdir = "/tmp/empty" + str(os.getpid())
            os.mkdir(tdir)
            tar=which("tar")
            with working_dir(tdir):
                # --mtime=@0 gives consistent tarfile checksum...
                tar("cf", "/tmp/empty.tar", ".", "--mtime=@0")
            os.rmdir(tdir)

        url = 'file:///tmp/empty.tar'
        return url


    def install(self, spec, prefix):
         libdir=''
         cdir = os.path.dirname(os.path.dirname(self.compiler.cxx))
         # find shortest pathname in cdir that has libstdc++.so in it...
         for path, dirnames, filenames in os.walk(cdir):
             if 'libstdc++.so' in filenames:
                 if not libdir or len(path) < len(libdir):
                     libdir = path
         if libdir:
             os.makedirs(prefix.lib)
             install_tree(libdir, prefix.lib)

    def setup_dependent_runtime_environment(self, env):
        env.append_flags("LDFLAGS", "-L"+self.prefix.lib)
