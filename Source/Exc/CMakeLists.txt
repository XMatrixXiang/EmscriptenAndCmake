
include(CMakeSources.cmake)


set(TargetName Exc)
# Targe
add_executable(${TargetName} ${Exc_SRC})

# Working directory
set_target_properties(${TargetName} PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY "$(OutDir)")	

# IDE specific
set_property(TARGET ${TargetName} PROPERTY FOLDER Exc)

# Includes
target_include_directories(${TargetName} PRIVATE "./")
