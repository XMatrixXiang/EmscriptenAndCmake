cmake_minimum_required (VERSION 3.9.0)
project (EmscriptenAndCmake)


set(SOURCE_DIR ${PROJECT_SOURCE_DIR}/Source/)

include(${SOURCE_DIR}/CMake/Properties.cmake)
include(${SOURCE_DIR}/CMake/FindPackageOrBuild.cmake)
include(${SOURCE_DIR}/CMake/HelperMethods.cmake)

add_subdirectory(${SOURCE_DIR}/Exc)