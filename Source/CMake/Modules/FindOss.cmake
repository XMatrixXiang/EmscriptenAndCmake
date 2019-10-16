# Find Oss dependency
#
# This module defines
#  Oss_INCLUDE_DIRS
#  Oss_LIBRARIES
#  Oss_FOUND

start_find_package(Oss)

set(Oss_INSTALL_DIR ${SOURCE_DIR}/../Dependencies/Oss CACHE PATH "")
gen_default_lib_search_dirs(Oss)


set(Oss_LIBNAME alibabacloud-oss-cpp-sdk)
	

find_imported_includes(Oss alibabacloud/oss/OssRequest.h)
find_imported_library(Oss ${Oss_LIBNAME})
end_find_package(Oss ${Oss_LIBNAME})

