# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *
from spack.util.elf import parse_elf


class CompilerRuntime(Package):
    """Package for compiler runtime libraries"""

    homepage = "https://gcc.gnu.org"
    has_code = False

    maintainers("haampie")

    license("GPL-3.0-only")

    version("1.0")

    requires("%gcc", "%clang")

    def install(self, spec, prefix):
        cc = Executable(self.compiler.cc)
        lib_regex = re.compile(rb"\blib[a-z-_]+\.so\.\d+\b")

        mkdir(prefix.lib)

        for name in ["atomic", "gcc_s", "gfortran", "gomp", "stdc++", "quadmath"]:
            # Look for the dynamic library that gcc would use to link,
            # that is with .so extension and without abi suffix.
            path = cc(f"--print-file-name=lib{name}.so", output=str).strip()

            # gcc reports an absolute path on success
            if not os.path.isabs(path):
                continue

            # Now there are two options:
            # 1. the file is an ELF file
            # 2. the file is a linker script referencing the actual library
            with open(path, "rb") as f:
                try:
                    # Try to parse as an ELF file
                    soname = parse_elf(f, dynamic_section=True).dt_soname_str.decode("utf-8")
                except Exception:
                    # On failure try to "parse" as ld script; the actual
                    # library needs to be mentioned by filename.
                    f.seek(0)
                    script_matches = lib_regex.findall(f.read())
                    if len(script_matches) != 1:
                        continue
                    soname = script_matches[0].decode("utf-8")

            # Now locate and install the runtime library
            runtime_path = cc(f"--print-file-name={soname}", output=str).strip()

            if not os.path.isabs(runtime_path):
                continue

            install(runtime_path, os.path.join(prefix.lib, soname))

    @property
    def libs(self):
        # Currently these libs are not linkable with -l, they all have a suffix.
        return LibraryList([])
