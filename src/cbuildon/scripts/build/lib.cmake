include(${CMAKE_CURRENT_LIST_DIR}/common.cmake)

add_library(${PROJECT_NAME}-Shared SHARED ${SRCS})
set_target_properties(${PROJECT_NAME}-Shared PROPERTIES OUTPUT_NAME ${PROJECT_NAME})
add_library(${PROJECT_NAME}-Static STATIC ${SRCS})
set_target_properties(${PROJECT_NAME}-Static PROPERTIES OUTPUT_NAME ${PROJECT_NAME})
