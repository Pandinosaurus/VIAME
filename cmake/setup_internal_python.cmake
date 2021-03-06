
set( PYTHON_FOUND TRUE CACHE INTERNAL "Forced" FORCE )

set( PYTHON_VERSION_MAJOR "3" CACHE INTERNAL "Forced" FORCE )
set( PYTHON_VERSION_MINOR "6" CACHE INTERNAL "Forced" FORCE )

set( PYTHON_INCLUDE_DIR ${VIAME_BUILD_INSTALL_PREFIX}/include CACHE PATH "Forced" FORCE )
if( WIN32 )
  set( PYTHON_EXECUTABLE ${VIAME_BUILD_INSTALL_PREFIX}/bin/python.exe CACHE PATH "Forced" FORCE )
  set( PYTHON_LIBRARY ${VIAME_BUILD_INSTALL_PREFIX}/lib/python3.lib CACHE PATH "Forced" FORCE )
else()
  set( PYTHON_EXECUTABLE ${VIAME_BUILD_INSTALL_PREFIX}/bin/python CACHE PATH "Forced" FORCE )
  set( PYTHON_LIBRARY ${VIAME_BUILD_INSTALL_PREFIX}/lib/libpython3.so CACHE PATH "Forced" FORCE )
endif()
