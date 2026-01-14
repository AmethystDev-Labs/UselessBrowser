# UselessBrowser

![UselessBrowser](docs/img/d09222c9-e25b-433c-afa0-f6161fe68bf5.jpeg)

基于 PyQt6 + Fluent UI 的指纹浏览器工作台，围绕 `spoofers + registration` 构建，提供更可控的隐私与指纹防护体验。

## 亮点

- 配置驱动：集中管理浏览器指纹配置，支持新建随机配置与基于 IP 的配置初始化。
- 一键安装：内置 Chrome for Testing 下载与管理，浏览器库清晰可查。
- 即时启动：选择配置与目标网址后即可启动浏览器。
- 防护齐全：WebRTC、Canvas、WebGL、音频、字体、地理位置、时区等多维度伪装。
- 易用界面：Fluent UI 风格，支持语言与主题设置。

## 快速开始

### 环境要求

- Python 3.12+
- Windows（推荐）
- 可选：`uv`（更快的依赖管理与启动）

### 安装依赖

```bash
uv sync
```

### 启动

```bash
uv run main.py
```

或直接使用：

```bat
start.bat
```

首次运行将进入新手引导，完成浏览器安装与配置初始化。

## 功能概览

- 主页：配置状态、快捷操作、卡片编辑。
- 启动：选择配置并打开目标网址。
- 配置：查看与管理指纹参数（UA、时区、语言、分辨率、WebGL、Canvas 等）。
- 浏览器库：展示本地与系统浏览器，支持安装/卸载。
- 设置：语言与主题切换。

## 目录结构

```
app/            # 核心 UI 与业务逻辑
profiles/       # 指纹配置数据
browsers/       # 浏览器安装目录
config/         # 应用配置
i18n/           # 多语言资源
docs/           # 文档与素材
```

## 技术栈

- PyQt6
- PyQt-Fluent-Widgets
- DrissionPage
- spoof

## 说明

本项目仍在迭代中，欢迎提出想法或建议。