import os,sys,io, subprocess

conan_ver = os.popen("conan -v").readlines()[0]
if ("2.0." in conan_ver):
    from conan import ConanFile
    from conan.tools.files import load, copy
    from conan.tools.cmake import CMake

    class Recipe(ConanFile):
        short_paths=True
        name = "cityhash"
        version = "##version_replace##"
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}
        generators = "CMakeToolchain"

        def layout(self):
        #     # The root of the project is one level above
        #     self.folders.root = "../.."
        #     # The source of the project (the root CMakeLists.txt) is the source folder
            self.folders.source = "."

        def config_options(self):
            if self.settings.os == "Windows":
                del self.options.fPIC

        def export_sources(self):
            # The path of the CMakeLists.txt and sources we want to export are one level above
            copy(self, "config*", os.path.join(self.recipe_folder, "../.."), self.export_sources_folder)
            copy(self, "CMakeLists.txt*", os.path.join(self.recipe_folder, ".."), self.export_sources_folder)
            copy(self, "cityhash*", os.path.join(self.recipe_folder, ".."), self.export_sources_folder)

        @property
        def _android_abi(self):
            return { "x86": "x86", "x86_64": "x86_64", "armv7": "armeabi-v7a", "armv8": "arm64-v8a"}.get(str(self.settings.arch))

        @property
        def _target_os(self):
            return { "Windows": "Windows", "Android": "Android", "Macos": "Darwin", "iOS": "iOS", "Linux": "Linux"}.get(str(self.settings.os))

        def build_requirements(self):
            pass

        def build(self):
            cmake_options = {
                "BUILD_SHARED_LIBS": False, 
                "ENABLE_CONAN_THIRD_LIBS": True, 
                "CMAKE_SYSTEM_NAME": self._target_os,
                "COMPILE_ENABLE_CITYHASH": True,
            }
            if self.settings.os == "Android":
                cmake_options["ANDROID_STL"] = "c++_shared"
                cmake_options["ANDROID_PLATFORM"] = "android-" + str(self.settings.os.api_level)
                cmake_options["ANDROID_ABI"] = self._android_abi,
                cmake_options["BUILD_SHARED_LIBS"] = False

            cmake = CMake(self)
            cmake.configure(variables=cmake_options)
            cmake.build()

        def package(self):
            copy(self, "*.h", os.path.join(self.export_sources_folder, "cityhash"), os.path.join(self.package_folder, "include/cityhash"), keep_path=False)
            src_lib_path = ["libs", "lib"]
            for lib_path in src_lib_path:
                copy(self, "*.lib",     os.path.join(self.build_folder, lib_path), os.path.join(self.package_folder, "lib"), keep_path=False)
                copy(self, "*.dll",     os.path.join(self.build_folder, lib_path), os.path.join(self.package_folder, "lib"), keep_path=False)
                copy(self, "*.pdb",     os.path.join(self.build_folder, lib_path), os.path.join(self.package_folder, "lib"), keep_path=False)
                copy(self, "*.so",      os.path.join(self.build_folder, lib_path), os.path.join(self.package_folder, "lib"), keep_path=False)
                copy(self, "*.dylib",   os.path.join(self.build_folder, lib_path), os.path.join(self.package_folder, "lib"), keep_path=False)
                copy(self, "*.a",       os.path.join(self.build_folder, lib_path), os.path.join(self.package_folder, "lib"), keep_path=False)

            copy(self, "*", os.path.join(self.build_folder, "bin"), os.path.join(self.package_folder, "bin"), keep_path=True)

        def package_info(self):
            liblist = []
            if os.path.isdir("lib"):
                for file in os.listdir("lib"):
                    if file.endswith('.lib') or file.endswith('.dll') or file.endswith('.a') or file.endswith('.so') or file.endswith('.dylib'):
                        if file not in self.cpp_info.libs:
                            self.cpp_info.libs.append(file)
else:
    from conans import ConanFile, CMake, tools
    class cityhashConan(ConanFile):
        short_paths=True
        name = "cityhash"
        version = "##version_replace##"
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}
        generators = "cmake"
        exports_sources = "../../config*", "../CMakeLists.txt*", "../../third_party/cityhash*"

        def config_options(self):
            if self.settings.os == "Windows":
                del self.options.fPIC

        def build_requirements(self):
            pass

        def requirements(self):
            pass

            if self.settings.os:
                pass
            if self.settings.os == "Windows":
                pass
            if self.settings.os == "Android":
                pass
            if self.settings.os == "Macos":
                pass
            if self.settings.os == "iOS":
                pass
            if self.settings.os == "Linux":
                pass
        @property
        def _android_abi(self):
            return { "x86": "x86", "x86_64": "x86_64", "armv7": "armeabi-v7a", "armv8": "arm64-v8a"}.get(str(self.settings.arch))

        @property
        def _target_os(self):
            return { "Windows": "Windows", "Android": "Android", "Macos": "Darwin", "iOS": "iOS", "Linux": "Linux"}.get(str(self.settings.os))

        def build(self):
            cmake = CMake(self)
            cmake.definitions["ENABLE_CONAN_THIRD_LIBS"] = True
            cmake.definitions["CMAKE_SYSTEM_NAME"] = self._target_os
            cmake.definitions["COMPILE_ENABLE_CITYHASH"] = True
            if self.settings.os == "Android":
                cmake.definitions["ANDROID_STL"] = "c++_shared"
                cmake.definitions["ANDROID_PLATFORM"] = "android-" + str(self.settings.os.api_level)
                cmake.definitions["ANDROID_ABI"] = self._android_abi
            cmake.configure(source_folder= "./", build_folder="./build", defs=cmake.definitions)
            cmake.build()

        def package(self):
            self.copy("*.h", dst="include/cityhash", src="cityhash/.", keep_path=False)
            src_lib_path = ["build/libs", "build/lib"]
            for lib_path in src_lib_path:
                self.copy("*.lib", dst="lib", src=lib_path, keep_path=False)
                self.copy("*.dll", dst="lib", src=lib_path, keep_path=False)
                self.copy("*.pdb", dst="lib", src=lib_path, keep_path=False)
                self.copy("*.so", dst="lib", src=lib_path, keep_path=False)
                self.copy("*.dylib", dst="lib", src=lib_path, keep_path=False)
                self.copy("*.a", dst="lib", src=lib_path, keep_path=False)

            self.copy("*", dst="bin", src="build/bin", keep_path=True)

            self.copy("*.apk", dst="bin", src="cityhash", keep_path=False)
        def package_info(self):
            liblist = []
            if os.path.isdir("lib"):
                for file in os.listdir("lib"):
                    if file.endswith('.lib') or file.endswith('.dll') or file.endswith('.a') or file.endswith('.so') or file.endswith('.dylib'):
                        if file not in self.cpp_info.libs:
                            self.cpp_info.libs.append(file)