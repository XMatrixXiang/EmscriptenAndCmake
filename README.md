# 简介
使用CMake构建C++项目，并且使用**Emscripten**转换成**Js**。
- 转换成js的脚本参考[**Ammo.js**]( https://github.com/kripken/ammo.js "Ammo github 地址")
- CMake构建参考[**bsf游戏引擎**](https://github.com/GameFoundry/bsf "bsf 游戏引擎 github地址")
- 使用[**WebIDL_bindings**](https://developer.mozilla.org/en-US/docs/Mozilla/WebIDL_bindings "") 进行C++到Js的导出

# PreRequest
- CMake
- Emscripten
- MinGW(Windows 系统下需要)
- python2.7

# 安装Emscripten
 1. 参考[**Emscripten**](https://emscripten.org/docs/getting_started/index.html "")官网的安装文档
# Build
- 进入到emsdk根目录（cd emsdk）
- 执行emsdk_env（ windows下执行 emsdk_env.bat Unix下执行 ./emsdk_env.sh）
- 切换到本项目的跟目录(cd E:/EmscriptenAndCmake)
- 执行python make.py (不出意外的话，在 根目录/Builds/JavaScriptSDK 下会看到**CadEngine.js**文件)))
  



