#!/bin/bash

# input：
#   os
#   buildtype: debug, release

if [[ "$1" != "Darwin" && "$1" != "iOS" && "$1" != "Android" && "$1" != "Linux" ]];then
    echo "dst os is not support: $1"
	exit 0
fi

if [[ -f tools/build/src/user-config.jam ]]; then
	rm -f tools/build/src/user-config.jam
fi

CURPATH=`pwd`

BUILD_TYPE="release"
if [[ "$2" = "Debug" || "$2" = "debug" ]];then
	BUILD_TYPE="debug"
fi

if [[ "$1" = "Android" ]];then

	ANDROID_NDK="/root/android-ndk-r16b"
	ANDROID_NDK_TOOLCHAIN_ROOT="${CURPATH}/ndk_toolchain"

	cat >> tools/build/src/user-config.jam <<EOF
using darwin : arm64 : ${ANDROID_NDK_TOOLCHAIN_ROOT}/bin/aarch64-linux-android-clang++ : 
<archiver>${ANDROID_NDK_TOOLCHAIN_ROOT}/bin/aarch64-linux-android-ar
<linker>${ANDROID_NDK_TOOLCHAIN_ROOT}/bin/llvm-link
<compileflags>--sysroot=${ANDROID_NDK_TOOLCHAIN_ROOT}/sysroot
<compileflags>-I${ANDROID_NDK_TOOLCHAIN_ROOT}/sysroot/usr/include/
<compileflags>-I${ANDROID_NDK_TOOLCHAIN_ROOT}/sysroot/usr/include/aarch64-linux-android/
;
EOF
elif [[ "$1" = "iOS" ]];then
	MIN_IOS_VERSION=12.0
	XCODE_ROOT=`xcode-select -print-path`
	IOS_SYSROOT=$XCODE_ROOT/Platforms/iPhoneOS.platform/Developer
	cat >> tools/build/src/user-config.jam <<EOF
using darwin : ios : clang++ -arch arm64 -isysroot $IOS_SYSROOT/SDKs/iPhoneOS.sdk -mios-version-min=$MIN_IOS_VERSION
: <striper> <root>$IOS_SYSROOT 
: <architecture>arm <target-os>iphone 
;
EOF
fi

if [ "$1" = "Android"  ];then
	rm -rf build_for_engine/lib
	rm -rf bin.v2
	rm -rf stage/lib/*
  python ${ANDROID_NDK}/build/tools/make_standalone_toolchain.py --arch arm64 --api 21 --stl=libc++ --install ${ANDROID_NDK_TOOLCHAIN_ROOT}

	./bootstrap.sh --with-toolset=clang
	rm project-config.jam
	cat bootstrap.log
  ./b2 stage -j 4 toolset=clang-arm64 architecture=arm target-os=android --without-python boost.locale.posix=off boost.locale.icu=off cxxflags="-std=c++14 -DANDROID_STL=c++_shared" link=static ${BUILD_TYPE} --stagedir=$3
fi

if [ "$1" = "Darwin" ];then
	rm -rf build_for_engine/lib
	rm -rf bin.v2
	rm -rf stage/lib/*
	./bootstrap.sh
	./b2 stage -j 4 target-os=darwin --without-python --without-process cxxflags="-stdlib=libc++" link=static ${BUILD_TYPE} --stagedir=$3
fi

if [ "$1" = "iOS"  ];then
	rm -rf build_for_engine/lib
	rm -rf bin.v2
	rm -rf stage/lib/*
	env -i ./bootstrap.sh
	rm project-config.jam
	./b2 stage  -j 4 toolset=darwin-ios abi=aapcs address-model=64 architecture=arm target-os=iphone --without-python --without-process cxxflags="-std=c++17 -stdlib=libc++" link=static ${BUILD_TYPE} --stagedir=$3
fi
