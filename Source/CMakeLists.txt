cmake_minimum_required(VERSION 3.10)
project(ThirdParty)
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

if (NOT THIRD_PARTY_SOURCE_DIR)
    set(THIRD_PARTY_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
endif()

include (${CMAKE_CURRENT_SOURCE_DIR}/../../CMake/Global.cmake)
set(THIRD_PARTY_FOLDER_CURRENT "ThirdParty")

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
# 默认值 自己改 给Boost用
set(VS_CMD_PATH "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat" CACHE PATH "VS_CMD_PATH")

option(COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS "COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS" OFF)

# 增加三方库的步骤如下

# 1、增加独立编译的开关
option(COMPILE_ENABLE_MIMALLOC "COMPILE_ENABLE_MIMALLOC" OFF)
option(COMPILE_ENABLE_EASTL "COMPILE_ENABLE_EASTL" OFF)
option(COMPILE_ENABLE_CITYHASH "COMPILE_ENABLE_CITYHASH" OFF)
option(COMPILE_ENABLE_ONETBB "COMPILE_ENABLE_ONETBB" OFF)
option(COMPILE_ENABLE_SPDLOG "COMPILE_ENABLE_SPDLOG" OFF)
option(COMPILE_ENABLE_UINT256_T "COMPILE_ENABLE_UINT256_T" OFF)
option(COMPILE_ENABLE_XXHASH "COMPILE_ENABLE_XXHASH" OFF)
option(COMPILE_ENABLE_BOOST "COMPILE_ENABLE_BOOST" OFF)

# 2、Include路径
# MIMALLOC
if (COMPILE_ENABLE_MIMALLOC OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    set(MI_BUILD_OBJECT OFF CACHE BOOL "" FORCE)
    set(MI_BUILD_STATIC OFF CACHE BOOL "" FORCE)
    set(MI_BUILD_TESTS OFF CACHE BOOL "" FORCE)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/mimalloc")
    set_target_properties("mimalloc" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY mimalloc)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/mimalloc/include")

# EASTL
if (COMPILE_ENABLE_EASTL OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    set(EASTL_BUILD_TESTS OFF CACHE BOOL "" FORCE)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/EASTL")
    set_target_properties("EASTL" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY EASTL)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/EASTL/include")

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
    set(TBBMALLOC_BUILD OFF CACHE BOOL "" FORCE)
    set(TBBMALLOC_PROXY_BUILD OFF CACHE BOOL "" FORCE)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/onetbb")
    set_target_properties("tbb" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY tbb)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/onetbb/include")

# SPDLOG 
if (COMPILE_ENABLE_SPDLOG OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    set(SPDLOG_BUILD_EXAMPLE OFF CACHE BOOL "" FORCE)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/spdlog")
    set_target_properties("spdlog" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY spdlog)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/spdlog/include")

# UINT256_T
if (COMPILE_ENABLE_UINT256_T OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/uint256_t")
    set_target_properties("uint256_t" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY uint256_t)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")

# CITYHASHC
if (COMPILE_ENABLE_CITYHASH OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/cityhash")
    set_target_properties("cityhash" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})
    list(APPEND THIRD_PARTY_DEPENDENCY cityhash)
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/cityhash/src")

# XXHASH
if (COMPILE_ENABLE_XXHASH OR COMPILE_ENABLE_ALL_THIRD_PARTY_LIBS)
    set(XXHASH_BUNDLED_MODE ON CACHE BOOL "" FORCE)
    set(XXHASH_BUILD_XXHSUM OFF CACHE BOOL "" FORCE)
    add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/xxhash/cmake_unofficial")
    set_target_properties("xxhash" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})
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
            COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/boost/build/$<CONFIG>/lib ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/$<CONFIG>)
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
            COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/boost/build/$<CONFIG>/lib ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/$<CONFIG>)
        add_dependencies(boost_copy boost_build)
        list(APPEND THIRD_PARTY_DEPENDENCY boost_copy)
    endif()
    set_target_properties("boost_build" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})
    set_target_properties("boost_copy" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})
endif()
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/boost")

# concurrentqueue
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")

# acl
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/acl/includes")
list(APPEND THIRD_PARTY_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/acl/external/rtm/includes")

# 3、Lib路径
if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    list(APPEND THIRD_PARTY_LIBS_DEBUG
        mimalloc.dll.lib
        EASTL.lib
        tbb12_debug.lib
        spdlogd.lib
        uint256_t.lib
        cityhash.lib
        xxhash.lib 
        libboost_atomic-vc143-mt-gd-x64-1_86.lib libboost_charconv-vc143-mt-gd-x64-1_86.lib libboost_chrono-vc143-mt-gd-x64-1_86.lib libboost_container-vc143-mt-gd-x64-1_86.lib libboost_context-vc143-mt-gd-x64-1_86.lib libboost_contract-vc143-mt-gd-x64-1_86.lib libboost_coroutine-vc143-mt-gd-x64-1_86.lib libboost_date_time-vc143-mt-gd-x64-1_86.lib libboost_exception-vc143-mt-gd-x64-1_86.lib libboost_fiber-vc143-mt-gd-x64-1_86.lib libboost_filesystem-vc143-mt-gd-x64-1_86.lib libboost_graph-vc143-mt-gd-x64-1_86.lib libboost_iostreams-vc143-mt-gd-x64-1_86.lib libboost_json-vc143-mt-gd-x64-1_86.lib libboost_locale-vc143-mt-gd-x64-1_86.lib libboost_log-vc143-mt-gd-x64-1_86.lib libboost_log_setup-vc143-mt-gd-x64-1_86.lib libboost_math_c99-vc143-mt-gd-x64-1_86.lib libboost_math_c99f-vc143-mt-gd-x64-1_86.lib libboost_math_c99l-vc143-mt-gd-x64-1_86.lib libboost_math_tr1-vc143-mt-gd-x64-1_86.lib libboost_math_tr1f-vc143-mt-gd-x64-1_86.lib libboost_math_tr1l-vc143-mt-gd-x64-1_86.lib libboost_nowide-vc143-mt-gd-x64-1_86.lib libboost_prg_exec_monitor-vc143-mt-gd-x64-1_86.lib libboost_process-vc143-mt-gd-x64-1_86.lib libboost_program_options-vc143-mt-gd-x64-1_86.lib libboost_random-vc143-mt-gd-x64-1_86.lib libboost_regex-vc143-mt-gd-x64-1_86.lib libboost_serialization-vc143-mt-gd-x64-1_86.lib libboost_stacktrace_from_exception-vc143-mt-gd-x64-1_86.lib libboost_stacktrace_noop-vc143-mt-gd-x64-1_86.lib libboost_stacktrace_windbg-vc143-mt-gd-x64-1_86.lib libboost_stacktrace_windbg_cached-vc143-mt-gd-x64-1_86.lib libboost_system-vc143-mt-gd-x64-1_86.lib libboost_test_exec_monitor-vc143-mt-gd-x64-1_86.lib libboost_thread-vc143-mt-gd-x64-1_86.lib libboost_timer-vc143-mt-gd-x64-1_86.lib libboost_type_erasure-vc143-mt-gd-x64-1_86.lib libboost_unit_test_framework-vc143-mt-gd-x64-1_86.lib libboost_url-vc143-mt-gd-x64-1_86.lib libboost_wave-vc143-mt-gd-x64-1_86.lib libboost_wserialization-vc143-mt-gd-x64-1_86.lib
    )
    list(APPEND THIRD_PARTY_LIBS_RELEASE
        mimalloc.dll.lib
        EASTL.lib
        tbb12.lib
        spdlog.lib
        uint256_t.lib
        cityhash.lib
        xxhash.lib 
        libboost_atomic-vc143-mt-x64-1_86.lib libboost_charconv-vc143-mt-x64-1_86.lib libboost_chrono-vc143-mt-x64-1_86.lib libboost_container-vc143-mt-x64-1_86.lib libboost_context-vc143-mt-x64-1_86.lib libboost_contract-vc143-mt-x64-1_86.lib libboost_coroutine-vc143-mt-x64-1_86.lib libboost_date_time-vc143-mt-x64-1_86.lib libboost_exception-vc143-mt-x64-1_86.lib libboost_fiber-vc143-mt-x64-1_86.lib libboost_filesystem-vc143-mt-x64-1_86.lib libboost_graph-vc143-mt-x64-1_86.lib libboost_iostreams-vc143-mt-x64-1_86.lib libboost_json-vc143-mt-x64-1_86.lib libboost_locale-vc143-mt-x64-1_86.lib libboost_log-vc143-mt-x64-1_86.lib libboost_log_setup-vc143-mt-x64-1_86.lib libboost_math_c99-vc143-mt-x64-1_86.lib libboost_math_c99f-vc143-mt-x64-1_86.lib libboost_math_c99l-vc143-mt-x64-1_86.lib libboost_math_tr1-vc143-mt-x64-1_86.lib libboost_math_tr1f-vc143-mt-x64-1_86.lib libboost_math_tr1l-vc143-mt-x64-1_86.lib libboost_nowide-vc143-mt-x64-1_86.lib libboost_prg_exec_monitor-vc143-mt-x64-1_86.lib libboost_process-vc143-mt-x64-1_86.lib libboost_program_options-vc143-mt-x64-1_86.lib libboost_random-vc143-mt-x64-1_86.lib libboost_regex-vc143-mt-x64-1_86.lib libboost_serialization-vc143-mt-x64-1_86.lib libboost_stacktrace_from_exception-vc143-mt-x64-1_86.lib libboost_stacktrace_noop-vc143-mt-x64-1_86.lib libboost_stacktrace_windbg-vc143-mt-x64-1_86.lib libboost_stacktrace_windbg_cached-vc143-mt-x64-1_86.lib libboost_system-vc143-mt-x64-1_86.lib libboost_test_exec_monitor-vc143-mt-x64-1_86.lib libboost_thread-vc143-mt-x64-1_86.lib libboost_timer-vc143-mt-x64-1_86.lib libboost_type_erasure-vc143-mt-x64-1_86.lib libboost_unit_test_framework-vc143-mt-x64-1_86.lib libboost_url-vc143-mt-x64-1_86.lib libboost_wave-vc143-mt-x64-1_86.lib libboost_wserialization-vc143-mt-x64-1_86.lib
    )
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Android")
    list(APPEND THIRD_PARTY_LIBS_DEBUG
        libtbb_debug.a
        libspdlogd.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_log.a libboost_log_setup.a libboost_math_c99.a libboost_math_c99f.a libboost_math_c99l.a libboost_math_tr1.a libboost_math_tr1f.a libboost_math_tr1l.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_basic.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )

    list(APPEND THIRD_PARTY_LIBS_RELEASE
        libtbb.a
        libspdlog.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_log.a libboost_log_setup.a libboost_math_c99.a libboost_math_c99f.a libboost_math_c99l.a libboost_math_tr1.a libboost_math_tr1f.a libboost_math_tr1l.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_basic.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    list(APPEND THIRD_PARTY_LIBS_DEBUG
        libtbb_debug.a
        libspdlogd.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_locale.a libboost_log.a libboost_log_setup.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_addr2line.a libboost_stacktrace_basic.a libboost_stacktrace_from_exception.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )

    list(APPEND THIRD_PARTY_LIBS_RELEASE
        libtbb.a
        libspdlog.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_locale.a libboost_log.a libboost_log_setup.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_addr2line.a libboost_stacktrace_basic.a libboost_stacktrace_from_exception.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )

elseif (${CMAKE_SYSTEM_NAME} MATCHES "iOS")
    list(APPEND THIRD_PARTY_LIBS_DEBUG
        libtbb_debug.a
        libspdlogd.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_locale.a libboost_log.a libboost_log_setup.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_addr2line.a libboost_stacktrace_basic.a libboost_stacktrace_from_exception.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )

    list(APPEND THIRD_PARTY_LIBS_RELEASE
        libtbb.a
        libspdlog.a
        libuint256_t.a
        libcityhash.a
        libxxhash.a
        libboost_atomic.a libboost_charconv.a libboost_chrono.a libboost_container.a libboost_context.a libboost_contract.a libboost_coroutine.a libboost_date_time.a libboost_exception.a libboost_fiber.a libboost_filesystem.a libboost_graph.a libboost_iostreams.a libboost_json.a libboost_locale.a libboost_log.a libboost_log_setup.a libboost_nowide.a libboost_prg_exec_monitor.a libboost_program_options.a libboost_random.a libboost_regex.a libboost_serialization.a libboost_stacktrace_addr2line.a libboost_stacktrace_basic.a libboost_stacktrace_from_exception.a libboost_stacktrace_noop.a libboost_system.a libboost_test_exec_monitor.a libboost_thread.a libboost_timer.a libboost_type_erasure.a libboost_unit_test_framework.a libboost_url.a libboost_wave.a libboost_wserialization.a
    )
endif()

set(THIRD_PARTY_INCLUDE_DIR ${THIRD_PARTY_INCLUDE_DIR} PARENT_SCOPE)
set(THIRD_PARTY_LIBS_DEBUG ${THIRD_PARTY_LIBS_DEBUG} PARENT_SCOPE)
set(THIRD_PARTY_LIBS_RELEASE ${THIRD_PARTY_LIBS_RELEASE} PARENT_SCOPE)
set(THIRD_PARTY_LIBS_DIR ${CMAKE_LIBRARY_OUTPUT_DIRECTORY} PARENT_SCOPE)

add_custom_target(ALL_THIRD_PARTY_BUILD ALL COMMAND ${CMAKE_COMMAND} -E echo "ALL_THIRD_PARTY_BUILD")
set_target_properties("ALL_THIRD_PARTY_BUILD" PROPERTIES FOLDER ${THIRD_PARTY_FOLDER_CURRENT})

if (NOT "${THIRD_PARTY_DEPENDENCY}" STREQUAL "")
    add_dependencies(ALL_THIRD_PARTY_BUILD ${THIRD_PARTY_DEPENDENCY})
endif()

macro(LinkThirdPartyLibs targetName)
    add_dependencies(${targetName} ALL_THIRD_PARTY_BUILD)
    target_include_directories(${targetName} PUBLIC ${THIRD_PARTY_INCLUDE_DIR})
    target_link_directories(${targetName} PUBLIC ${THIRD_PARTY_LIBS_DIR})
    target_link_libraries(${targetName} PUBLIC $<IF:$<CONFIG:Debug>, ${THIRD_PARTY_LIBS_DEBUG}, ${THIRD_PARTY_LIBS_RELEASE}>)
endmacro()