include(${{CMAKE_CURRENT_LIST_DIR}}/lib.cmake)

link_directories(${{{projectNamePrefix}_LIB_DIR}})
set(CMAKE_CXX_FLAGS "${{CMAKE_CXX_FLAGS}} ${{{projectNamePrefix}_CXX_FLAGS}}")
message("CMAKE_CXX_FLAGS=${{CMAKE_CXX_FLAGS}}")
set({projectNamePrefix}_TESTS_ROOT_PATH ${{{projectNamePrefix}_PROJECT_ROOT_PATH}}/tests)
include_directories(${{{projectNamePrefix}_TESTS_ROOT_PATH}})

set({projectNamePrefix}_TEST_NAMES)
list(APPEND {projectNamePrefix}_TEST_NAMES )

foreach(testName IN LISTS {projectNamePrefix}_TEST_NAMES)
  add_executable(${{testName}} ${{{projectNamePrefix}_TESTS_ROOT_PATH}}/${{testName}}.cpp)
  target_link_libraries(${{testName}} {projectName}-static)
endforeach()
