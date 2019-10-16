# Find Curl dependency
#
# This module defines
#  Curl_INCLUDE_DIRS
#  Curl_LIBRARIES
#  Curl_FOUND

start_find_package(Curl)

set(Curl_INSTALL_DIR ${SOURCE_DIR}/../Dependencies/Curl CACHE PATH "")
gen_default_lib_search_dirs(Curl)
if(WIN32)
	set(libcurl libcurl)
elseif(LINUX)
	set(libcurl curl)
endif()

find_imported_includes(Curl curl/curl.h)
find_imported_library_shared(Curl ${libcurl})
install_dependency_binaries(Curl)
end_find_package(Curl ${libcurl})

