# FileTree Visualizer

![Snipaste_2025-03-02_13-57-47](https://github.com/user-attachments/assets/f63401ed-baf1-4226-ab7d-7c5f3e7b2229)

## 项目概述

**FileTree Visualizer** 是一款轻量级的文件树管理器和目录可视化工具，专为提升用户与AI（如ChatGPT、DeepSeek、Claude、Grok等）交互体验而设计。通过简单的拖放操作，用户可以快速生成标准化的文件目录结构，帮助AI更精准地理解文件上下文关系，减少因复杂文件结构导致的理解偏差。

> **💡 专业提示**: 向AI提供清晰的文件结构可以显著提高其理解复杂项目或资源组织的能力，从而获得更精准的回答和建议。

## 项目背景与初衷

在与AI进行交互过程中，清晰的上下文信息对于获取准确回答至关重要。特别是在需要提供文件或资源目录结构时，手动整理往往耗时且容易出错。FileTree Visualizer正是为解决这一痛点而生，它通过图形化界面和标准化的文本输出，将复杂的文件夹结构转化为清晰、易读的格式，如下所示：

```
资速达创业资源大礼包
├── AI工具资源
│   ├── DeepSeek全家桶资源
│   │   ├── DeepSeek 100+种身份扮演.pdf
│   │   ├── DeepSeek 万能提问模板-.pdf
│   │   └── 《7天精通DeepSeek实操手册》.pdf
│   ├── 【技能分享】AI+学习，我发现 AI+人，真的可以加速知行合一的"知".pdf
│   └── 我用 AI 工作流写了一篇文章，单日收益 4722.pdf
├── 创业工具与商机
│   ├── 万字长文说透 AI 代写公文月入五位数的底层逻辑！.txt
│   └── 私域认知笔记-从0开始教你搭建私域认知体系.pdf
└── 0-大礼包使用指南.pdf
```

这种结构化的输出不仅方便用户快速整理资源，还能显著提升AI处理复杂任务时的准确性和效率。

## 核心功能特性

FileTree Visualizer提供一系列强大而直观的功能，帮助用户轻松管理和共享文件结构：

✅ **文件夹拖放支持**  
&nbsp;&nbsp;&nbsp;&nbsp;支持将文件夹直接拖入界面，自动解析并生成文件树，操作简单直观

✅ **实时刷新功能**  
&nbsp;&nbsp;&nbsp;&nbsp;支持对已加载文件夹进行一键刷新，无需重复拖入相同文件夹即可更新目录结构

✅ **双面板可视化设计**  
&nbsp;&nbsp;&nbsp;&nbsp;左侧提供交互式树状结构展示，右侧生成格式化文本表示，满足不同使用需求

✅ **一键复制功能**  
&nbsp;&nbsp;&nbsp;&nbsp;生成格式化的文本目录树，支持一键复制，方便直接粘贴至AI对话框或文档

✅ **丰富的右键菜单**  
&nbsp;&nbsp;&nbsp;&nbsp;支持在文件结构可视化界面中通过右键菜单复制文件名称、相对路径或绝对路径

✅ **双主题模式**  
&nbsp;&nbsp;&nbsp;&nbsp;内置深色和浅色主题，适应不同使用环境和个人偏好

✅ **轻量级设计**  
&nbsp;&nbsp;&nbsp;&nbsp;程序体积小，运行高效，无需复杂配置，开箱即用

## 应用场景

FileTree Visualizer 在多种场景下具有广泛的实用价值：

### 与AI交互场景

* **AI提问优化**  
  为AI提供清晰的目录结构，显著提升问答质量和深度，特别适用于：
  - 代码项目分析和重构咨询
  - 学习资料组织评估
  - 文件系统优化建议

* **编程和开发辅助**  
  帮助AI理解项目结构，从而获得更精准的编程建议：
  - 项目结构分析
  - 代码组织优化
  - 架构设计评估

### 工作和学习场景

* **资源管理**  
  快速整理和可视化个人或团队的文件资源：
  - 研究资料整理
  - 项目文件管理
  - 学习资源分类

* **文档编写**  
  生成标准化目录结构，用于：
  - 技术文档编写
  - 项目说明文档
  - 资源目录清单

* **知识分享与协作**  
  在分享资料或项目时，提供清晰的内容概览：
  - 学习资料分享
  - 软件包内容说明
  - 团队项目交接

## 安装与使用指南

### 方法一：获取可执行程序

目前您可以通过以下方式获取可直接运行的程序：

* **关注微信公众号【资速达】**
* **回复关键词【FT】**获取Windows exe可执行文件下载地址

这是获取已编译版本的最便捷方式，下载后无需任何配置，解压即可使用。

### 方法二：从源代码运行

如果您希望自行运行源代码或进行定制化修改，请按以下步骤操作：

1. **安装必备库**：

```bash
pip install PySide6 pyperclip
```

2. **运行程序**：

```bash
python file-tree-visualizer.py
```

### 方法三：自行打包应用

若您希望创建自己的可执行文件，可使用PyInstaller进行打包：

```bash
pyinstaller --onefile --windowed --icon=icon.ico file-tree-visualizer.py
```

注意：GitHub仓库仅包含源代码，不提供预编译的可执行文件。如需立即使用，建议选择方法一或方法二。

## 使用方法

### 基本操作流程

1. **启动应用**  
   双击运行可执行文件，程序会以默认暗色主题启动

2. **加载文件夹**  
   有三种方式可以加载文件夹：
   - 直接将文件夹拖入应用界面（推荐）
   - 点击工具栏中的"选择文件夹"按钮
   - 使用系统文件选择对话框浏览并选择目标文件夹

3. **查看目录结构**  
   - 左侧面板显示交互式树状可视化结构，包含文件类型、修改时间和大小信息
   - 右侧面板显示标准化的文本格式输出，可直接用于与AI交互

4. **复制文本结构**  
   点击右侧面板下方的"复制到剪贴板"按钮，将文本格式的目录结构复制到系统剪贴板

5. **更新目录结构**  
   如需更新目录结构（例如文件有变动），点击工具栏中的"刷新"按钮即可，无需重新拖入文件夹

6. **使用右键菜单功能**  
   在左侧树状图中，右键点击任意文件或文件夹，可以：
   - 复制文件或文件夹名称
   - 复制相对路径（相对于根目录）
   - 复制绝对路径（完整系统路径）
   - 在系统文件浏览器中打开所选项目

7. **切换主题**  
   点击工具栏中的"切换主题"按钮可在暗色和亮色主题之间切换

## 技术实现

FileTree Visualizer采用现代化的技术架构，基于Python和PySide6（Qt for Python）框架开发，提供跨平台的图形用户界面体验。

### 核心技术栈

- **Python**: 作为主要开发语言，提供高效的文件系统处理能力
- **PySide6**: Qt框架的Python绑定，用于构建美观且功能丰富的桌面应用界面
- **文件系统操作**: 利用Python标准库中的os模块处理文件和目录结构
- **树形数据可视化**: 通过QTreeWidget组件实现直观的目录结构展示
- **拖放功能**: 支持文件夹拖放操作，提升用户体验
- **暗色/亮色主题**: 内置主题切换系统，适应不同使用环境
- **SVG矢量图标**: 使用可缩放的矢量图标，确保在任何分辨率下都清晰显示

该应用采用模块化设计，主要功能区块包括：

- 文件树视图模块
- 文本输出处理模块
- 用户交互界面模块
- 主题管理系统
- 上下文菜单功能

程序在设计上注重性能优化和用户体验，即使处理大型目录结构也能保持高效运行。

## 项目状态与许可协议

### 开发状态

本软件由**Claude 3.7 Sonnet Model**协助编写代码，已完成核心功能开发并作为稳定版本发布。作者将其分享至开源社区，遵循开源精神，但目前处于维护模式：

- ✅ 核心功能已完成并稳定运行
- ✅ 已进行跨平台兼容性测试
- ✅ 支持Windows、macOS和Linux系统
- ⚠️ 不接受新功能请求
- ⚠️ 不提供定期更新承诺

### 许可协议

本项目采用**MIT许可证**，这是一种宽松的开源软件许可协议：

- ✅ 允许任何人自由使用、复制和修改软件
- ✅ 可以将软件作为独立项目或商业产品的一部分使用
- ✅ 唯一的要求是在软件的所有副本中都必须包含原始许可证和版权声明
- ✅ 软件按"原样"提供，无任何明示或暗示的保证

### 使用声明

- 此工具设计用于合法的个人和教育用途
- 严禁将本工具用于任何非法活动或侵犯他人权益的行为
- 用户对使用本软件的行为及其后果承担全部责任
- 软件不收集任何用户数据，完全在本地运行

### 技术支持

本项目为一次性开源分享，采用有限支持模式：

- ⚠️ 不提供个人技术支持或问题排查
- ⚠️ 不接受功能定制或付费开发请求
- ✅ 用户可自行修改源代码以适应特定需求
- ✅ 欢迎在遵循MIT许可的前提下进行分发和改进

### 联系方式

如需了解更多相关资源和工具：

- 关注微信公众号【资速达】获取更多AI和效率工具资讯
- GitHub仓库问题追踪功能仅用于报告关键问题，不保证及时响应
