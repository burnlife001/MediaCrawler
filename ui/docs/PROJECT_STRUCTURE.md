# MediaCrawler UI 项目结构

## 📁 完整目录结构

```
MediaCrawler/
├── 📁 ui/                           # UI模块（完整的图形界面系统）
│   ├── 📁 components/               # UI组件
│   │   ├── config_panel.py          # 配置面板（2x2布局）
│   │   ├── progress_panel.py        # 进度面板（实时状态）
│   │   └── result_panel.py          # 结果面板（表格显示）
│   ├── 📁 controllers/              # 控制器
│   │   ├── url_parser.py            # URL解析器（支持分享文本）
│   │   ├── crawler_controller.py    # 爬虫控制器（异步处理）
│   │   └── data_processor.py        # 数据处理器（智能导出）
│   ├── 📁 utils/                    # 工具类
│   │   ├── config_manager.py        # 配置管理器（data目录）
│   │   ├── dependency_checker.py    # 依赖检查器（启动前检查）
│   │   └── ui_helpers.py            # UI辅助函数
│   ├── 📁 scripts/                  # 脚本文件
│   │   └── launch_ui.py             # UI启动脚本（完整版）
│   ├── 📁 tests/                    # 测试文件
│   │   └── test_all.py              # 综合测试脚本
│   ├── 📁 docs/                     # 文档
│   │   ├── README_UI.md             # 详细使用说明
│   │   └── PROJECT_STRUCTURE.md     # 项目结构说明（本文件）
│   ├── main_window.py               # 主窗口（核心UI）
│   ├── app.py                       # 应用入口（依赖检查）
│   ├── ui_prd.md                    # 产品需求文档
│   └── README.md                    # UI模块说明
├── 📁 data/                         # 数据目录
│   ├── ui_config.json               # UI配置文件 ⭐
│   └── 📁 ui_exports/               # UI导出文件目录
│       └── crawl_result_*.xlsx      # 爬取结果文件
├── launch_ui.py                     # 简化启动脚本（根目录）
├── requirements.txt                 # 依赖列表（包含UI依赖）
└── ... (其他MediaCrawler原有文件)
```

## 🎯 核心模块说明

### 📱 UI组件 (components/)
- **config_panel.py**: 配置面板，2x2布局，包含登录方式、爬取设置、评论设置、代理设置
- **progress_panel.py**: 进度面板，显示实时状态、进度条、统计信息、运行日志
- **result_panel.py**: 结果面板，表格形式显示爬取结果，支持实时更新

### 🎮 控制器 (controllers/)
- **url_parser.py**: URL解析器，支持抖音分享文本解析、短链接处理、格式验证
- **crawler_controller.py**: 爬虫控制器，集成MediaCrawler逻辑，异步爬取处理
- **data_processor.py**: 数据处理器，智能导出策略、会话文件管理、格式转换

### 🔧 工具类 (utils/)
- **config_manager.py**: 配置管理器，保存到data目录，默认抖音平台，持久化设置
- **dependency_checker.py**: 依赖检查器，启动前检查、自动安装、详细报告
- **ui_helpers.py**: UI辅助函数，通用UI工具和辅助方法

### 📜 脚本文件 (scripts/)
- **launch_ui.py**: 完整启动脚本，包含依赖检查、错误处理、用户指导

### 🧪 测试文件 (tests/)
- **test_all.py**: 综合测试脚本，覆盖所有核心功能的测试

### 📖 文档 (docs/)
- **README_UI.md**: 详细使用说明，包含安装、配置、使用教程
- **PROJECT_STRUCTURE.md**: 项目结构说明（本文件）

## 🚀 启动方式

### 方式一：根目录启动（推荐）
```bash
python launch_ui.py
```

### 方式二：UI目录启动
```bash
python ui/scripts/launch_ui.py
```

### 方式三：自动安装依赖启动
```bash
python launch_ui.py --auto-install
```

## 🧪 测试方式

### 综合测试
```bash
python ui/tests/test_all.py
```

### 依赖检查
```bash
python ui/utils/dependency_checker.py
```

## 📦 依赖管理

### UI必需依赖
- **tkinter**: GUI界面库（Python内置）
- **pandas**: 数据处理和Excel导出
- **openpyxl**: Excel文件读写
- **httpx**: HTTP客户端（短链接解析）
- **playwright**: 浏览器自动化
- **pydantic**: 数据验证库
- **tenacity**: 重试机制库
- **parsel**: HTML/XML解析器
- **pyexecjs**: JavaScript执行引擎
- **requests**: HTTP请求库
- **aiofiles**: 异步文件操作

### 安装方式
```bash
# 推荐：安装所有依赖（包含MediaCrawler核心依赖）
pip install -r requirements.txt

# 注意：请确保在虚拟环境中运行安装命令
```

## 🎨 设计特点

### 模块化设计
- 清晰的目录结构
- 功能模块分离
- 易于维护和扩展

### 用户友好
- 启动前依赖检查
- 详细的错误提示
- 完整的使用文档

### 生产就绪
- 完整的测试覆盖
- 错误处理机制
- 配置持久化

## 🔄 开发流程

### 添加新功能
1. 在相应目录创建新模块
2. 在主窗口中集成
3. 添加测试用例
4. 更新文档

### 修复问题
1. 运行测试定位问题
2. 修复相关代码
3. 验证测试通过
4. 更新相关文档

### 发布版本
1. 运行完整测试套件
2. 更新版本号
3. 更新文档
4. 创建发布包

## 📈 未来扩展

### 可能的扩展方向
- 支持更多平台（B站、微博等）
- 增加数据分析功能
- 添加定时任务功能
- 支持批量处理
- 增加云端同步功能
