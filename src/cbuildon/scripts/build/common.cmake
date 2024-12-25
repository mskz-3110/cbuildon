message("CXX_FLAGS=${CXX_FLAGS}")
message("LIB_DIR=${LIB_DIR}")
set(PROJECT_ROOT_PATH ${CMAKE_CURRENT_LIST_DIR}/..)
set(SRC_ROOT_PATH ${PROJECT_ROOT_PATH}/src)
set(SRCS)
list(APPEND SRCS ${SRC_ROOT_PATH}/{SRC}) # Rename SRC

set(INCS)
list(APPEND INCS ${PROJECT_ROOT_PATH}/inc)
include_directories(${INCS})
