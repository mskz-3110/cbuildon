include(${{CMAKE_CURRENT_LIST_DIR}}/common.cmake)

add_library({projectName}-shared SHARED ${{{projectNamePrefix}_SRCS}})
set_target_properties({projectName}-shared PROPERTIES OUTPUT_NAME {projectName})
add_library({projectName}-static STATIC ${{{projectNamePrefix}_SRCS}})
set_target_properties({projectName}-static PROPERTIES OUTPUT_NAME {projectName})
