
@echo off

:: Determine source tree and build tree
setlocal
set "SOURCE=%~dp0"
set "SOURCE=%SOURCE:~0,-1%\.."
set "BUILD="
if "%~1" == "" goto :continue
set "ARG1=%~1"
if "%ARG1:~0,1%" equ "-" goto :continue
set "BUILD=%~1"
shift
:continue
if "%BUILD%" == "" (echo Usage: %~nx0 \path\to\build-tree [build-options] && exit /B 1)

:: Detect CMake toolchains directory if it is not provided explicitly
if "%TOOLCHAINS%" == "" set "TOOLCHAINS=%SOURCE%\Source\CMake\Toolchains"

:: Default to native generator and toolchain if none is specified explicitly
set "OPTS="
set "BUILD_OPTS="
set "arch="
:loop
if not "%~1" == "" (   
    if "%~1" == "-DWEB" if "%~2" == "1" set "OPTS=-G "MinGW Makefiles" -DCMAKE_TOOLCHAIN_FILE="%TOOLCHAINS%\Emscripten.cmake""        
    if "%~1" == "-G" set "OPTS=%OPTS% %~1 %2"
    set "ARG1=%~1"
    set "ARG2=%~2"
    if "%ARG1:~0,2%" == "-D" set "BUILD_OPTS=%BUILD_OPTS% %ARG1%=%ARG2%"
    shift
    shift
    goto loop
)
if exist "%BUILD%\CMakeCache.txt" set "OPTS="

:: Create project with the chosen CMake generator and toolchain
cmake -E make_directory "%BUILD%" && cmake -E chdir "%BUILD%" cmake %OPTS% %BUILD_OPTS% "%SOURCE%"
