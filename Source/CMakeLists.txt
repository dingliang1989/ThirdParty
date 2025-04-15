cmake_minimum_required(VERSION 3.10)

project(ThirdParty)

set(ENGINE_FOLDER_CURRENT "ThirdParty")

option(INCLUDE_TOOLCHAIN_FILE_ENABLE "INCLUDE_TOOLCHAIN_FILE_ENABLE" OFF)
if (CMAKE_TOOLCHAIN_FILE AND INCLUDE_TOOLCHAIN_FILE_ENABLE)
    message("CMAKE_TOOLCHAIN_FILE: ${CMAKE_TOOLCHAIN_FILE}")
    include(${CMAKE_TOOLCHAIN_FILE})
endif()

############################################################################
if (CMAKE_SYSTEM_NAME)
    set(DST_SYSTEM_NAME ${CMAKE_SYSTEM_NAME})
else()
    set(DST_SYSTEM_NAME ${CMAKE_HOST_SYSTEM_NAME})
endif()

if (DST_SYSTEM_NAME MATCHES "Android")
    set(DST_ABI ${ANDROID_ABI})
elseif (DST_SYSTEM_NAME MATCHES "Windows")
    if (CMAKE_CL_64)
        set(DST_ABI "x64")
    else()
        set(DST_ABI "x86")
    endif()
endif()
##########################COMPILE_OPTIONS####################################
if (NOT BUILD_SHARED_LIBS)
    set(BUILD_SHARED_LIBS OFF)
endif()

add_compile_options(-Ot)

#set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,--gc-sections")
if (${DST_SYSTEM_NAME} MATCHES "Windows")
    add_compile_options(/std:c++20 /Zi /MP /WX- /W2)
else()
    if (${DST_SYSTEM_NAME} MATCHES "Android")
        add_definitions("-DANDROID_STL=c++_shared")
    endif()
    add_compile_options(-std=c++20 -ffunction-sections -fdata-sections)
endif()

if (${DST_SYSTEM_NAME} MATCHES "iOS")
    add_compile_options(-fobjc-abi-version=2 -fobjc-arc)
endif()

if(${DST_SYSTEM_NAME} MATCHES "iOS" OR ${DST_SYSTEM_NAME} MATCHES "Darwin")
    # clang 14后默认会打开werror，需要手动关闭
    add_compile_options(-Wno-error)
endif()

#目前符号不能隐藏，没有完整的符号导出机制，打包的时候会把多余的符号剔除
#add_compile_options(-fvisibility=hidden -fvisibility-inlines-hidden)
add_compile_options(-D__STDC_FORMAT_MACROS)
if (NOT ${DST_SYSTEM_NAME} MATCHES "Windows")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g")
endif()

########################### OUTDIR ##########################################
set(CMAKE_SHARED_LIBRARY_RUNTIME_C_FLAG "-Wl,-rpath,")

####################function############################
function(FolderTra_GetCode result rootdir)
    file(GLOB allcode "${rootdir}/*")
    set(${result} ${allcode} PARENT_SCOPE)
endfunction()

function(FolderTraRCS_GetCode result rootdir)
    file(GLOB_RECURSE allcode "${rootdir}/*")
    set(${result} ${allcode} PARENT_SCOPE)
endfunction()

function(SrcCodeGroup rootdir root_dir_name)
    FolderTraRCS_GetDir(dirlist ${rootdir})
    foreach(dir ${dirlist})
        FolderTra_GetCode(dircode ${dir})
        list(LENGTH dircode len)    
        if (NOT (${dir} STREQUAL ${rootdir}))  
            string(REPLACE "${rootdir}" "" groupname ${dir})
            #message("${root_dir_name}/${groupname}     ${len}")
            if (${len} STRGREATER 0)  
                source_group(${root_dir_name}/${groupname} FILES ${dircode})
            endif()
        else()
            #message("/     ${len}")
            if (${len} STRGREATER 0) 
                source_group(${root_dir_name} FILES ${dircode})
            endif()
        endif()
        
    endforeach()
endfunction()

function(FolderTraRCS_GetDir result rootdir)
    LIST(APPEND alldir ${rootdir})
    file(GLOB_RECURSE all LIST_DIRECTORIES true ${rootdir}/*)
    foreach(fileordir ${all})
        if (IS_DIRECTORY ${fileordir})    
            LIST(APPEND alldir ${fileordir})
        endif()
    endforeach()
    set(${result} ${alldir} PARENT_SCOPE)
endfunction()
############################################################################
set(THIRD_PARTY_LIBS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../Libraries)

if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    add_compile_options(/FS)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${THIRD_PARTY_LIBS_DIR}/${CMAKE_SYSTEM_NAME}/$<CONFIG>)
    set(CMAKE_COMPILE_PDB_OUTPUT_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})
endif()
if (${CMAKE_SYSTEM_NAME} MATCHES "Android")
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${THIRD_PARTY_LIBS_DIR}/${CMAKE_SYSTEM_NAME}/${ANDROID_ABI}/${CMAKE_BUILD_TYPE})
endif()
if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    add_compile_options(-Wno-shorten-64-to-32)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${THIRD_PARTY_LIBS_DIR}/${CMAKE_SYSTEM_NAME}/$<CONFIG>)
endif()
if (${CMAKE_SYSTEM_NAME} MATCHES "iOS")
    add_compile_options(-Wno-shorten-64-to-32)
    add_definitions(-DBOOST_NO_CXX98_FUNCTION_BASE)
    set(CMAKE_OSX_ARCHITECTURES arm64)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${THIRD_PARTY_LIBS_DIR}/${CMAKE_SYSTEM_NAME}/$<CONFIG>)
endif()

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})
set(CMAKE_MACOSX_RPATH ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/\$\{CONFIGURATION\})

set(CMAKE_C_FLAGS ${CMAKE_CXX_FLAGS})
set(CMAKE_C_FLAGS_DEBUG ${CMAKE_CXX_FLAGS_DEBUG})
set(CMAKE_C_FLAGS_RELEASE ${CMAKE_CXX_FLAGS_RELEASE})

# 默认值 自己改 给Boost用
set(VS_CMD_PATH "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat" CACHE PATH "VS_CMD_PATH")

option(COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS "COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS" OFF)

# 增加三方库的步骤如下

# 1、增加独立编译的开关
option(COMPILE_ENABLE_CITYHASH "COMPILE_ENABLE_CITYHASH" OFF)
option(COMPILE_ENABLE_ONETBB "COMPILE_ENABLE_ONETBB" OFF)
option(COMPILE_ENABLE_SPDLOG "COMPILE_ENABLE_SPDLOG" OFF)
option(COMPILE_ENABLE_UINT256_T "COMPILE_ENABLE_UINT256_T" OFF)
option(COMPILE_ENABLE_XXHASH "COMPILE_ENABLE_XXHASH" OFF)
option(COMPILE_ENABLE_BOOST "COMPILE_ENABLE_BOOST" OFF)

# 2、Include路径
# ONETBB
if (COMPILE_ENABLE_ONETBB OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    if (${DST_ABI} MATCHES "armeabi-v7a")
        add_definitions("-D__aarch32__")
    endif()
    if (${CMAKE_SYSTEM_NAME} MATCHES "Android")
        set(ANDROID_NDK_MAJOR 16)
    endif()
    add_definitions("-D__TBB_SOURCE_DIRECTLY_INCLUDED=1")
    set(TBB_TEST OFF CACHE BOOL "" FORCE)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/onetbb")
    set_target_properties("tbb" PROPERTIES FOLDER ${ENGINE_FOLDER_CURRENT})
    set_target_properties("tbbmalloc" PROPERTIES FOLDER ${ENGINE_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY tbb tbbmalloc)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/onetbb/include")

# SPDLOG 
if (COMPILE_ENABLE_SPDLOG OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    set(SPDLOG_BUILD_EXAMPLE OFF CACHE BOOL "" FORCE)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/spdlog")
    set_target_properties("spdlog" PROPERTIES FOLDER ${ENGINE_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY spdlog)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/spdlog/include")

# UINT256_T
if (COMPILE_ENABLE_UINT256_T OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/uint256_t")
    set_target_properties("uint256_t" PROPERTIES FOLDER ${ENGINE_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY uint256_t)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")

# CITYHASHC
if (COMPILE_ENABLE_CITYHASH OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/cityhash")
    set_target_properties("cityhash" PROPERTIES FOLDER ${ENGINE_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY cityhash)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/cityhash/src")

# XXHASH
if (COMPILE_ENABLE_XXHASH OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    set(XXHASH_BUNDLED_MODE ON CACHE BOOL "" FORCE)
    set(XXHASH_BUILD_XXHSUM OFF CACHE BOOL "" FORCE)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/xxhash/cmake_unofficial")
    set_target_properties("xxhash" PROPERTIES FOLDER ${ENGINE_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY xxhash)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")

# BOOST
if (COMPILE_ENABLE_BOOST OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
        add_custom_target(boost_build ALL
            COMMAND cmd.exe /c "\"${VS_CMD_PATH}\" && bootstrap.bat && cd ${CMAKE_CURRENT_SOURCE_DIR}/boost && b2.exe stage architecture=x86 address-model=64 link=static cxxflags=/std:c++20 $<IF:$<CONFIG:Debug>, debug, release> --stagedir=build/$<CONFIG>"
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/boost)
        add_custom_target(boost_copy ALL
            COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/boost/build/$<CONFIG>/lib/cmake
            COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/boost/build/$<CONFIG>/lib ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})
        add_dependencies(boost_copy boost_build)
        list(APPEND THIRD_PARTY_DEPENDENCY boost_copy)
    elseif (${CMAKE_SYSTEM_NAME} MATCHES "Android")
        # Android Windows编译不过，需要在linux上编译，因此直接保留2进制在output目录下
    elseif (${CMAKE_SYSTEM_NAME} MATCHES "Darwin" OR ${CMAKE_SYSTEM_NAME} MATCHES "iOS")
        add_custom_target(boost_build ALL
            COMMAND /bin/zsh build_for_engine/build.sh ${CMAKE_SYSTEM_NAME} $<CONFIG> build/$<CONFIG>
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/boost)
        add_custom_target(boost_copy ALL
            COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/boost/build/$<CONFIG>/lib/cmake
            COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/boost/build/$<CONFIG>/lib ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})
        add_dependencies(boost_copy boost_build)
        list(APPEND THIRD_PARTY_DEPENDENCY boost_copy)
    endif()
    set_target_properties("boost_build" PROPERTIES FOLDER ${ENGINE_FOLDER_CURRENT})
    set_target_properties("boost_copy" PROPERTIES FOLDER ${ENGINE_FOLDER_CURRENT})
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/boost")

# concurrentqueue
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")

# acl
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/acl/includes")

set(THIRD_PARTY_INCLUDE_DIR ${THIRD_PARTY_INCLUDE_DIR} PARENT_SCOPE)
set(THIRD_PARTY_LIBS_DIR ${THIRD_PARTY_LIBS_DIR} PARENT_SCOPE)

# 2、Lib路径
if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    list(APPEND THIRD_PARTY_LIBS_DEBUG
        tbbmalloc_debug.lib tbb12_debug.lib
        spdlogd.lib
        uint256_t.lib
        cityhash.lib
        xxhash.lib 
        libboost_atomic-vc143-mt-gd-x64-1_86.lib libboost_charconv-vc143-mt-gd-x64-1_86.lib libboost_chrono-vc143-mt-gd-x64-1_86.lib libboost_container-vc143-mt-gd-x64-1_86.lib libboost_context-vc143-mt-gd-x64-1_86.lib libboost_contract-vc143-mt-gd-x64-1_86.lib libboost_coroutine-vc143-mt-gd-x64-1_86.lib libboost_date_time-vc143-mt-gd-x64-1_86.lib libboost_exception-vc143-mt-gd-x64-1_86.lib libboost_fiber-vc143-mt-gd-x64-1_86.lib libboost_filesystem-vc143-mt-gd-x64-1_86.lib libboost_graph-vc143-mt-gd-x64-1_86.lib libboost_iostreams-vc143-mt-gd-x64-1_86.lib libboost_json-vc143-mt-gd-x64-1_86.lib libboost_locale-vc143-mt-gd-x64-1_86.lib libboost_log-vc143-mt-gd-x64-1_86.lib libboost_log_setup-vc143-mt-gd-x64-1_86.lib libboost_math_c99-vc143-mt-gd-x64-1_86.lib libboost_math_c99f-vc143-mt-gd-x64-1_86.lib libboost_math_c99l-vc143-mt-gd-x64-1_86.lib libboost_math_tr1-vc143-mt-gd-x64-1_86.lib libboost_math_tr1f-vc143-mt-gd-x64-1_86.lib libboost_math_tr1l-vc143-mt-gd-x64-1_86.lib libboost_nowide-vc143-mt-gd-x64-1_86.lib libboost_prg_exec_monitor-vc143-mt-gd-x64-1_86.lib libboost_process-vc143-mt-gd-x64-1_86.lib libboost_program_options-vc143-mt-gd-x64-1_86.lib libboost_random-vc143-mt-gd-x64-1_86.lib libboost_regex-vc143-mt-gd-x64-1_86.lib libboost_serialization-vc143-mt-gd-x64-1_86.lib libboost_stacktrace_from_exception-vc143-mt-gd-x64-1_86.lib libboost_stacktrace_noop-vc143-mt-gd-x64-1_86.lib libboost_stacktrace_windbg-vc143-mt-gd-x64-1_86.lib libboost_stacktrace_windbg_cached-vc143-mt-gd-x64-1_86.lib libboost_system-vc143-mt-gd-x64-1_86.lib libboost_test_exec_monitor-vc143-mt-gd-x64-1_86.lib libboost_thread-vc143-mt-gd-x64-1_86.lib libboost_timer-vc143-mt-gd-x64-1_86.lib libboost_type_erasure-vc143-mt-gd-x64-1_86.lib libboost_unit_test_framework-vc143-mt-gd-x64-1_86.lib libboost_url-vc143-mt-gd-x64-1_86.lib libboost_wave-vc143-mt-gd-x64-1_86.lib libboost_wserialization-vc143-mt-gd-x64-1_86.lib
    )
    list(APPEND THIRD_PARTY_LIBS_RELEASE
        tbbmalloc.lib tbb12.lib
        spdlog.lib
        uint256_t.lib
        cityhash.lib
        xxhash.lib 
        libboost_atomic-vc143-mt-x64-1_86.lib libboost_charconv-vc143-mt-x64-1_86.lib libboost_chrono-vc143-mt-x64-1_86.lib libboost_container-vc143-mt-x64-1_86.lib libboost_context-vc143-mt-x64-1_86.lib libboost_contract-vc143-mt-x64-1_86.lib libboost_coroutine-vc143-mt-x64-1_86.lib libboost_date_time-vc143-mt-x64-1_86.lib libboost_exception-vc143-mt-x64-1_86.lib libboost_fiber-vc143-mt-x64-1_86.lib libboost_filesystem-vc143-mt-x64-1_86.lib libboost_graph-vc143-mt-x64-1_86.lib libboost_iostreams-vc143-mt-x64-1_86.lib libboost_json-vc143-mt-x64-1_86.lib libboost_locale-vc143-mt-x64-1_86.lib libboost_log-vc143-mt-x64-1_86.lib libboost_log_setup-vc143-mt-x64-1_86.lib libboost_math_c99-vc143-mt-x64-1_86.lib libboost_math_c99f-vc143-mt-x64-1_86.lib libboost_math_c99l-vc143-mt-x64-1_86.lib libboost_math_tr1-vc143-mt-x64-1_86.lib libboost_math_tr1f-vc143-mt-x64-1_86.lib libboost_math_tr1l-vc143-mt-x64-1_86.lib libboost_nowide-vc143-mt-x64-1_86.lib libboost_prg_exec_monitor-vc143-mt-x64-1_86.lib libboost_process-vc143-mt-x64-1_86.lib libboost_program_options-vc143-mt-x64-1_86.lib libboost_random-vc143-mt-x64-1_86.lib libboost_regex-vc143-mt-x64-1_86.lib libboost_serialization-vc143-mt-x64-1_86.lib libboost_stacktrace_from_exception-vc143-mt-x64-1_86.lib libboost_stacktrace_noop-vc143-mt-x64-1_86.lib libboost_stacktrace_windbg-vc143-mt-x64-1_86.lib libboost_stacktrace_windbg_cached-vc143-mt-x64-1_86.lib libboost_system-vc143-mt-x64-1_86.lib libboost_test_exec_monitor-vc143-mt-x64-1_86.lib libboost_thread-vc143-mt-x64-1_86.lib libboost_timer-vc143-mt-x64-1_86.lib libboost_type_erasure-vc143-mt-x64-1_86.lib libboost_unit_test_framework-vc143-mt-x64-1_86.lib libboost_url-vc143-mt-x64-1_86.lib libboost_wave-vc143-mt-x64-1_86.lib libboost_wserialization-vc143-mt-x64-1_86.lib
    )
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Android")
    list(APPEND THIRD_PARTY_LIBS_DEBUG
        libtbb_debug.a libtbbmalloc_debug.a
        libspdlogd.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_log.a libboost_log_setup.a libboost_math_c99.a libboost_math_c99f.a libboost_math_c99l.a libboost_math_tr1.a libboost_math_tr1f.a libboost_math_tr1l.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_basic.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )

    list(APPEND THIRD_PARTY_LIBS_RELEASE
        libtbb.a libtbbmalloc.a
        libspdlog.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_log.a libboost_log_setup.a libboost_math_c99.a libboost_math_c99f.a libboost_math_c99l.a libboost_math_tr1.a libboost_math_tr1f.a libboost_math_tr1l.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_basic.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    list(APPEND THIRD_PARTY_LIBS_DEBUG
        libtbb_debug.a libtbbmalloc_debug.a
        libspdlogd.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_locale.a libboost_log.a libboost_log_setup.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_addr2line.a libboost_stacktrace_basic.a libboost_stacktrace_from_exception.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )

    list(APPEND THIRD_PARTY_LIBS_RELEASE
        libtbb.a libtbbmalloc.a
        libspdlog.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_locale.a libboost_log.a libboost_log_setup.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_addr2line.a libboost_stacktrace_basic.a libboost_stacktrace_from_exception.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )

elseif (${CMAKE_SYSTEM_NAME} MATCHES "iOS")
    list(APPEND THIRD_PARTY_LIBS_DEBUG
        libtbb_debug.a libtbbmalloc_debug.a
        libspdlogd.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_locale.a libboost_log.a libboost_log_setup.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_addr2line.a libboost_stacktrace_basic.a libboost_stacktrace_from_exception.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )

    list(APPEND THIRD_PARTY_LIBS_RELEASE
        libtbb.a libtbbmalloc.a
        libspdlog.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_locale.a libboost_log.a libboost_log_setup.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_addr2line.a libboost_stacktrace_basic.a libboost_stacktrace_from_exception.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )
endif()

set(THIRD_PARTY_LIBS_DEBUG ${THIRD_PARTY_LIBS_DEBUG} PARENT_SCOPE)
set(THIRD_PARTY_LIBS_RELEASE ${THIRD_PARTY_LIBS_RELEASE} PARENT_SCOPE)

add_custom_target(ALL_THIRD_PARTY_BUILD ALL COMMAND ${CMAKE_COMMAND} -E echo "ALL_THIRD_PARTY_BUILD")
set_target_properties("ALL_THIRD_PARTY_BUILD" PROPERTIES FOLDER ${ENGINE_FOLDER_CURRENT})

if (NOT "${THIRD_PARTY_DEPENDENCY}" STREQUAL "")
    add_dependencies(ALL_THIRD_PARTY_BUILD ${THIRD_PARTY_DEPENDENCY})
endif()