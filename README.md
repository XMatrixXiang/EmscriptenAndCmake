# 简介

使用**CMake**构建**C/C++**项目，并且使用**Emscripten**转换成**javaScript**。

- 转换成**JavaScript**的脚本**make.py**参考[**Ammo.js**]( https://github.com/kripken/ammo.js "Ammo github 地址")
- **CMake**构建参考[**bsf游戏引擎**](https://github.com/GameFoundry/bsf "bsf 游戏引擎 github地址")
- 使用[**WebIDL_bindings**](https://developer.mozilla.org/en-US/docs/Mozilla/WebIDL_bindings "") 进行C++到Js的导出

## PreRequest

- **CMake**（*安装CMake 3.16 以上版本，备注中有linux下安装cmake3.16.0的安装方法*）
- **Emscripten**
- **MinGW(*Windows 系统下需要*)**
- **python2.7**

## 安装Emscripten

 1. 参考[**Emscripten**](https://emscripten.org/docs/getting_started/index.html "")官网的安装文档

## Build

- 进入到**emsdk**根目录（**cd emsdk**）
- 执行**emsdk_env**（ windows下执行 emsdk_env.bat Unix下执行 **source ./emsdk_env.sh**）
- 切换到本项目的根目录(**cd E:/EmscriptenAndCmake**)
- 执行**python make.py** (不出意外的话，在 **根目录/Builds/JavaScriptSDK** 下会看到**CadEngine.js**文件)

## 备注

### **Cmake**在linxu的安装

- wget [https://cmake.org/files/v3.16/cmake-3.16.0-rc1-Linux-x86_64.tar.gz](https://cmake.org/files/v3.16/cmake-3.16.0-rc1-Linux-x86_64.tar.gz,"Cmake3.16.0")
- tar -zxvf cmake-3.16.0.tar.gz
- cd cmake-3.16.0
- ./configure
- make
- make install

## 相关链接

- [webidl](https://heycam.github.io/webidl "webidl")
- [WebIDL bindings](https://developer.mozilla.org/en-US/docs/Mozilla/WebIDL_bindings "WebIDL bindings")
  