# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Triton(CMakePackage):
    """Triton Client Libraries and Examples"""

    homepage = "https://github.com/triton-inference-server/client"
    url = "https://github.com/triton-inference-server/client/archive/refs/heads/r23.09.zip"

    maintainers("marcmengel")

    version( "23.09", sha256="33ece9b6a0ee3c6b198afde5e955ec53bb5c2c30eafbb80f9bd940619f14307b")

    variant("cuda", default=False)

    depends_on("curl")
    depends_on("abseil-cpp")
    depends_on("protobuf", type=("build", "run"))
    depends_on("cuda", type=("build", "run"), when="+cuda")
    depends_on("googletest", type=("build", "run"))
    depends_on("rapidjson", type=("build", "run"))
    depends_on("grpc", type=("build", "run"))
    depends_on("re2", type=("build", "run"))
    depends_on("c-ares", type=("build", "run"))
    depends_on("openssl", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-grpcio", type=("build", "run"))
    depends_on("py-grpcio-tools", type=("build", "run"))
    depends_on("py-numpy")
    depends_on("py-geventhttpclient")
    depends_on("py-python-rapidjson")

    def patch(self):
        # clean out all the third-party stuff...
        filter_file( r'^ *-D[^C].*:PATH.*', '', 'CMakeLists.txt')
        filter_file( r'^ *-DC[^M].*:PATH.*', '', 'CMakeLists.txt')
        filter_file( r'FetchContent_MakeAvailable\(repo-third-party\)', '', 'CMakeLists.txt')

        filter_file( r'DEPENDS \${_.._client_depends}', '', 'CMakeLists.txt')
        filter_file( r'FetchContent_MakeAvailable\(googletest\)', 'find_package(googletest)', 'src/c++/CMakeLists.txt')

        
    @run_after('cmake')
    def postpatch(self):
        # this package writes a cmake_isntall.cmake that tries to put
        # external third-party bits (which we aren't building) in the
        # destination, so run an initial make that will fail, and then
        # clean them out
        with working_dir(self.build_directory):
            try:
                make("all")
            except:
                pass
            filter_file(
                r'".*library/\.\./\.\./third-party.*"',
                '',
                'cc-clients/library/cmake_install.cmake'
            )

    def url_for_version(self, version):
        urlf = "https://github.com/triton-inference-server/client/archive/refs/heads/r{0}.zip"
        return urlf.format(version)

    # root_cmakelists_dir = "src/c++"

    def cmake_args(self):
        args = [
            "-DTRITON_COMMON_REPO_TAG=r{0}".format(self.spec.version),
            "-DTRITON_THIRD_PARTY_REPO_TAG=r{0}".format(self.spec.version),
            "-DTRITON_CORE_REPO_TAG=r{0}".format(self.spec.version),
            "-DTRITON_ENABLE_CC_HTTP=ON",
            "-DTRITON_ENABLE_CC_GRPC=ON",
            "-DTRITON_ENABLE_JAVA_HTTP=OFF",
            "-DTRITON_ENABLE_PYTHON_HTTP=ON",
            "-DTRITON_ENABLE_PYTHON_GRPC=ON",
            "-DThreads_FOUND=ON",
            "-DCMAKE_THREAD_LIBS_INIT=-lpthread",
            "-DCMAKE_USE_PTHREADS_INIT=ON",
            "-DTRITON_USE_THIRD_PARTY=OFF",
            "-DCMAKE_INSTALL_LOCAL_ONLY=ON",
        ]

        if "+cuda" in self.spec:
            args.append("-DTRITON_ENABLE_GPU:BOOL=ON")
            args.append("-DTRITON_ENABLE_METRICS_GPU:BOOL=ON")
        else:
            args.append("-DTRITON_ENABLE_GPU:BOOL=OFF")
            args.append("-DTRITON_ENABLE_METRICS_GPU:BOOL=OFF")

        return args

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            flags.append("-I{0}".format(self.spec['rapidjson'].prefix.include))
        elif name == "ldflags":
            flags.append("-L{0}".format(self.spec['rapidjson'].prefix.lib64))
            flags.append("-L/lib64")
        return (flags, None, None)

