include(ExternalProject)
set(EXTERNAL_INSTALL_LOCATION ${CMAKE_BINARY_DIR}/external)

ExternalProject_Add(gtest-project
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG main
  CMAKE_ARGS
  -DCMAKE_INSTALL_PREFIX=${EXTERNAL_INSTALL_LOCATION}
  -DCMAKE_INSTALL_RPATH=${EXTERNAL_INSTALL_LOCATION}/lib
  -DCMAKE_CXX_FLAGS=-fPIC
  INSTALL_COMMAND make install
)

install(DIRECTORY "${EXTERNAL_INSTALL_LOCATION}/include" DESTINATION ${CMAKE_INSTALL_PREFIX})
install(DIRECTORY "${EXTERNAL_INSTALL_LOCATION}/lib" DESTINATION ${CMAKE_INSTALL_PREFIX})

SET(GCC_TEST_COMPILE_FLAGS "-g -O0 -fprofile-arcs -ftest-coverage")
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g -O0 -fprofile-arcs -ftest-coverage")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GCC_TEST_COMPILE_FLAGS}" )

enable_testing()
add_subdirectory(${PROJECT_SOURCE_DIR}/src/test)
