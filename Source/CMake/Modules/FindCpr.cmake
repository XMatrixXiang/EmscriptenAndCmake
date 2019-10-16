# Find Cpr dependency
#
# This module defines
#  Cpr_INCLUDE_DIRS
#  Cpr_LIBRARIES
#  Cpr_FOUND

start_find_package(Cpr)

set(Cpr_INSTALL_DIR ${SOURCE_DIR}/../Dependencies/Cpr CACHE PATH "")
gen_default_lib_search_dirs(Cpr)


set(Cpr_LIBNAME cpr)
	

find_imported_includes(Cpr cpr/api.h)
find_imported_library(Cpr ${Cpr_LIBNAME})
end_find_package(Cpr ${Cpr_LIBNAME})

