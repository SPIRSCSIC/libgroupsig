# Test suites

# Tests for GL19
add_executable(GL19Test test_gl19.cpp)
target_link_libraries(GL19Test
  PUBLIC
  groupsig
  big
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME GL19Test COMMAND GL19Test)

# Tests for BBS04
add_executable(BBS04Test test_bbs04.cpp)
target_link_libraries(BBS04Test
  PUBLIC
  groupsig
  big
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME BBS04Test COMMAND BBS04Test)

# Tests for CPY06
#add_executable(CPY06Test test_cpy06.cpp)
#target_link_libraries(CPY06Test
#  PUBLIC
#  groupsig
#  big
#  sys
#  logger
#  gtest_main
#  gtest
#  pthread)
#add_test(NAME CPY06Test COMMAND CPY06Test)

# Tests for PS16
add_executable(PS16Test test_ps16.cpp)
target_link_libraries(PS16Test
  PUBLIC
  groupsig
  big
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME PS16Test COMMAND PS16Test)

# Tests for KLAP20
add_executable(KLAP20Test test_klap20.cpp)
target_link_libraries(KLAP20Test
  PUBLIC
  groupsig
  big
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME KLAP20Test COMMAND KLAP20Test)

# Tests for DL21
add_executable(DL21Test test_dl21.cpp)
target_link_libraries(DL21Test
  PUBLIC
  groupsig
  big
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME DL21Test COMMAND DL21Test)

# Tests for DL21SEQ
add_executable(DL21SEQTest test_dl21seq.cpp)
target_link_libraries(DL21SEQTest
  PUBLIC
  groupsig
  big
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME DL21SEQTest COMMAND DL21SEQTest)

# Tests for PBC
add_executable(PBCTest test_pbc.cpp)
target_link_libraries(PBCTest
  PUBLIC
  pbcext
  base64
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME PBCTest COMMAND PBCTest)

# Tests for Hash
add_executable(HashTest test_hash.cpp)
target_link_libraries(HashTest
  PUBLIC
  hash
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME HashTest COMMAND HashTest)

# Tests for KTY04
add_executable(KTY04Test test_kty04.cpp)
target_link_libraries(KTY04Test
  PUBLIC
  groupsig
  big
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME KTY04Test COMMAND KTY04Test)

# Tests for Bigz
add_executable(BigzTest test_bigz.cpp)
target_link_libraries(BigzTest
  PUBLIC
  big
  sys
  logger
  gtest_main
  gtest
  pthread)
add_test(NAME BigzTest COMMAND BigzTest)

add_custom_target(check COMMAND ${CMAKE_CTEST_COMMAND} --verbose)
