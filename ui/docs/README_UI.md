# MediaCrawler UI 使用说明

## 📋 项目简介

MediaCrawler UI 是一个图形化的抖音和小红书评论提取工具，提供直观的用户界面，支持分享文本解析、实时爬取和自动数据导出。

## 🚀 快速开始

### 1. 环境要求

- **Python版本**: 3.7 或更高版本
- **操作系统**: Windows、macOS、Linux
- **内存**: 建议 4GB 以上
- **网络**: 需要稳定的网络连接

### 2. 安装依赖

#### 方法一：自动检查和安装
```bash
# 启动时自动检查依赖，如有缺失会提示安装
python launch_ui.py

# 或者使用自动安装模式
python launch_ui.py --auto-install
```

#### 方法二：手动安装
```bash
# 安装所有依赖
pip install -r requirements.txt

# 或者单独安装关键依赖
pip install pandas openpyxl Pillow httpx playwright
```

#### 方法三：依赖检查
```bash
# 单独运行依赖检查
python ui/utils/dependency_checker.py

# 详细测试
python test_dependency_check.py
```

### 3. 启动程序

```bash
# 标准启动
python launch_ui.py

# 自动安装缺失依赖
python launch_ui.py --auto-install
```

## 🎯 主要功能

### 📱 智能URL处理
- **分享文本解析**: 自动从抖音分享文本中提取URL
- **多格式支持**: 标准链接、短链接、分享链接
- **实时验证**: 输入时即时验证和状态反馈
- **智能按钮**: 只有解析成功才能开始爬取

### 🤖 完整爬虫集成
- **浏览器自动化**: 基于Playwright的自动化
- **登录管理**: 支持二维码、Cookie、手机号登录
- **短链接处理**: 运行时自动重定向获取真实ID
- **异步处理**: 高效的异步爬取机制

### 📊 智能数据管理
- **实时显示**: 表格形式展示爬取结果
- **自动导出**: 100条数据自动导出Excel
- **会话管理**: 单一文件累计所有数据
- **多格式支持**: Excel、CSV、JSON导出

### 🎨 优化的用户界面
- **紧凑布局**: 配置和进度信息并排显示
- **实时反馈**: 状态显示、进度条、运行日志
- **响应式设计**: 支持窗口最大化和缩放
- **用户友好**: 直观的操作流程

## 📖 使用教程

### 基本使用流程

1. **启动程序**
   ```bash
   python launch_ui.py
   ```

2. **输入视频链接**
   - 直接粘贴抖音分享文本
   - 或输入标准视频链接
   - 点击"解析"按钮验证

3. **配置爬取设置**
   - 选择登录方式（推荐二维码）
   - 设置评论数量限制
   - 配置爬取间隔

4. **开始爬取**
   - 点击"开始爬取"按钮
   - 实时查看进度和结果
   - 自动导出Excel文件

### 高级功能

#### 代理设置
- 启用代理选项
- 输入代理地址（格式：http://ip:port）
- 支持HTTP/HTTPS代理

#### 数据导出
- **自动导出**: 100条数据自动保存
- **手动导出**: 随时点击"导出数据"
- **文件位置**: `data/ui_exports/` 目录
- **文件命名**: `crawl_result_YYYYMMDD_HHMMSS.xlsx`

#### 配置管理
- **配置文件**: `data/ui_config.json`
- **自动保存**: 设置自动持久化
- **默认平台**: 抖音(dy)

## 🔧 故障排除

### 常见问题

#### 1. 依赖缺失错误
```
❌ 缺少必要的依赖包: No module named 'PIL'
```
**解决方案**:
```bash
# 自动安装
python launch_ui.py --auto-install

# 或手动安装
pip install Pillow
```

#### 2. 启动失败
```
❌ 依赖检查失败，无法启动程序
```
**解决方案**:
```bash
# 检查Python版本
python --version

# 重新安装依赖
pip install -r requirements.txt

# 运行依赖测试
python test_dependency_check.py
```

#### 3. 浏览器问题
```
❌ 浏览器启动失败
```
**解决方案**:
```bash
# 安装浏览器
playwright install

# 或安装特定浏览器
playwright install chromium
```

#### 4. 网络连接问题
- 检查网络连接
- 尝试使用代理
- 调整爬取间隔

### 日志查看

程序运行时会在界面显示详细日志，包括：
- 依赖检查结果
- URL解析状态
- 爬取进度信息
- 错误和警告信息

## 📁 项目结构

```
MediaCrawler/
├── ui/                          # UI模块
│   ├── components/              # UI组件
│   ├── controllers/             # 控制器
│   ├── utils/                   # 工具类
│   ├── main_window.py           # 主窗口
│   └── app.py                   # 应用入口
├── data/                        # 数据目录
│   ├── ui_config.json          # UI配置文件
│   └── ui_exports/             # 导出文件目录
├── launch_ui.py                # UI启动脚本
├── requirements.txt            # 依赖列表
└── README_UI.md               # 使用说明
```

## 🎉 更新日志

### v1.0.0 (2025-06-18)
- ✅ 完整的UI界面实现
- ✅ 智能依赖检查系统
- ✅ 抖音分享文本解析
- ✅ 自动数据导出
- ✅ 配置文件管理
- ✅ 错误处理和用户指导

## 📞 技术支持

如果遇到问题，请：

1. **检查依赖**: 运行 `python test_dependency_check.py`
2. **查看日志**: 注意界面中的错误信息
3. **重新安装**: 使用 `pip install -r requirements.txt`
4. **更新浏览器**: 运行 `playwright install`

## 📄 许可证

本项目遵循原MediaCrawler项目的许可证条款。
