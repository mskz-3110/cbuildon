include(${CMAKE_CURRENT_LIST_DIR}/lib.cmake)

link_directories(${LIB_DIR})
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CXX_FLAGS}")
message("CMAKE_CXX_FLAGS=${CMAKE_CXX_FLAGS}")
set(TESTS_ROOT_PATH ${PROJECT_ROOT_PATH}/tests)
include_directories(${TESTS_ROOT_PATH})
set(TEST_NAMES)
list(APPEND TEST_NAMES {TEST_NAME}) # Rename TEST_NAME
foreach(testName IN LISTS TEST_NAMES)
  add_executable(${testName} ${TESTS_ROOT_PATH}/${testName}.cpp)
  target_link_libraries(${testName} ${PROJECT_NAME}-Static)
endforeach()
