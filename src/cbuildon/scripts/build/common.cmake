message("{projectNamePrefix}_CXX_FLAGS=${{{projectNamePrefix}_CXX_FLAGS}}")
message("{projectNamePrefix}_LIB_DIR=${{{projectNamePrefix}_LIB_DIR}}")
set({projectNamePrefix}_PROJECT_ROOT_PATH ${{CMAKE_CURRENT_LIST_DIR}}/..)
include_directories(${{{projectNamePrefix}_PROJECT_ROOT_PATH}}/inc)
set({projectNamePrefix}_SRC_ROOT_PATH ${{{projectNamePrefix}_PROJECT_ROOT_PATH}}/src)

set({projectNamePrefix}_SRCS)
list(APPEND {projectNamePrefix}_SRCS ${{{projectNamePrefix}_SRC_ROOT_PATH}}/)
