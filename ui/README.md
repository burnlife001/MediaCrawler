# MediaCrawler UI 模块

## 📁 目录结构

```
ui/
├── components/              # UI组件
│   ├── config_panel.py      # 配置面板
│   ├── progress_panel.py    # 进度面板
│   └── result_panel.py      # 结果面板
├── controllers/             # 控制器
│   ├── url_parser.py        # URL解析器
│   ├── crawler_controller.py # 爬虫控制器
│   └── data_processor.py    # 数据处理器
├── utils/                   # 工具类
│   ├── config_manager.py    # 配置管理器
│   ├── dependency_checker.py # 依赖检查器
│   └── ui_helpers.py        # UI辅助函数
├── scripts/                 # 脚本文件
│   └── launch_ui.py         # UI启动脚本
├── tests/                   # 测试文件
│   └── test_all.py          # 综合测试脚本
├── docs/                    # 文档
│   └── README_UI.md         # 详细使用说明
├── main_window.py           # 主窗口
├── app.py                   # 应用入口
├── ui_prd.md               # 产品需求文档
└── README.md               # 本文件
```

## 🚀 快速启动

### 从项目根目录启动
```bash
python launch_ui.py
```

### 从UI目录启动
```bash
python scripts/launch_ui.py
```

### 运行测试
```bash
python ui/tests/test_all.py
```

## 📖 详细文档

请查看 [详细使用说明](docs/README_UI.md) 获取完整的使用指南。

## 🧪 测试

UI模块包含完整的测试套件：

- **依赖检查测试**: 验证所有必需依赖
- **URL解析测试**: 验证抖音分享文本解析
- **数据处理测试**: 验证数据添加和导出
- **配置管理测试**: 验证配置保存和加载
- **UI组件测试**: 验证所有UI组件导入

## 🔧 开发

### 添加新组件
1. 在 `components/` 目录创建新组件
2. 在 `main_window.py` 中集成组件
3. 添加相应的测试

### 添加新控制器
1. 在 `controllers/` 目录创建新控制器
2. 在相应的UI组件中使用
3. 更新测试套件

### 添加新工具
1. 在 `utils/` 目录创建新工具类
2. 在需要的地方导入使用
3. 添加单元测试
