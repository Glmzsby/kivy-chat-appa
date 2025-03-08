# Mobile Chat App

[![Build Android APK](https://github.com/{你的用户名}/{仓库名}/actions/workflows/build.yml/badge.svg)](https://github.com/{你的用户名}/{仓库名}/actions/workflows/build.yml)

一个基于Kivy的移动聊天客户端。

## 构建状态

GitHub Actions会自动构建Android APK文件。你可以在以下位置找到构建好的APK：

1. 进入 [Actions页面](https://github.com/{你的用户名}/{仓库名}/actions)
2. 点击最新的构建记录
3. 在"Artifacts"部分下载构建好的APK文件

## 使用方法

1. 将代码克隆到本地：
```bash
git clone https://github.com/{你的用户名}/{仓库名}.git
cd {仓库名}
```

2. 推送更改到GitHub：
```bash
git add .
git commit -m "更新代码"
git push
```

3. 等待GitHub Actions自动构建APK（大约需要10-15分钟）

4. 在Actions页面下载构建好的APK文件

## 本地构建

如果你想在本地构建APK，请按照以下步骤操作：

1. 安装必要的依赖：
```bash
sudo apt-get install python3-pip build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
```

2. 安装Python依赖：
```bash
pip install buildozer
pip install cython
```

3. 构建APK：
```bash
buildozer android debug
```

构建完成后，APK文件将位于`bin/`目录下。

## 许可证

[MIT License](LICENSE)