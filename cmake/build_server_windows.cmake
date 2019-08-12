set(CTEST_SITE "zeah.kitware.com")
set(CTEST_BUILD_NAME "Windows7_GPU_Master_Nightly")
set(CTEST_SOURCE_DIRECTORY "C:/workspace/VIAME-master_WinNight")
set(CTEST_BINARY_DIRECTORY "C:/workspace/VIAME-master_WinNight/build/")
set(CTEST_CMAKE_GENERATOR "Visual Studio 15 2017 Win64")
#set(CTEST_CMAKE_GENERATOR "Visual Studio 15 2017")
#set(CTEST_CMAKE_GENERATOR_PLATFORM "x64")
set(CTEST_BUILD_CONFIGURATION Release)
set(CTEST_PROJECT_NAME VIAME)
set(CTEST_BUILD_MODEL "Nightly")
set(CTEST_NIGHTLY_START_TIME "3:00:00 UTC")
set(CTEST_USE_LAUNCHERS 1)
include(CTestUseLaunchers)
set(OPTIONS 
  "-DCMAKE_BUILD_TYPE=Release"
  "-DCUDA_TOOLKIT_ROOT_DIR=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.0"
  "-DCUDNN_ROOT_DIR:PATH=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.0/lib/x64"
  "-DVIAME_CREATE_PACKAGE=ON"
  "-DVIAME_ENABLE_CUDNN=ON"
  "-DVIAME_ENABLE_CUDA=ON"
  "-DVIAME_ENABLE_CAMTRAWL=ON"
  "-DVIAME_ENABLE_PYTHON=ON"
  "-DVIAME_ENABLE_GDAL=ON"
  "-DVIAME_ENABLE_SCALLOP_TK=OFF"
  "-DVIAME_ENABLE_PYTORCH=ON"
  "-DVIAME_BUILD_INTERNAL_PYTORCH=ON"
  "-DVIAME_KWIVER_BUILD_DIR=C:/tmp/kv1"
)

set(platform Windows7)
