# Find Openssl dependency
#
# This module defines
#  Openssl_INCLUDE_DIRS
#  Openssl_LIBRARIES
#  Openssl_FOUND

start_find_package(Openssl)

set(Openssl_INSTALL_DIR ${SOURCE_DIR}/../Dependencies/Openssl CACHE PATH "")
gen_default_lib_search_dirs(Openssl)


set(Openssl_LIBNAME libcurl)
set(eay32_LIBNAME libeay32)
set(ssleay32_LIBNAME ssleay32)

find_imported_includes(Openssl aes.h)
find_imported_library(Openssl ${Oss_LIBNAME})
find_imported_library(Openssl ${eay32_LIBNAME})
find_imported_library(Openssl ${ssleay32_LIBNAME})
end_find_package(Openssl ${Oss_LIBNAME})

