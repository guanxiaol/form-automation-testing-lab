# Windsurf Registration Automation Lab（安全版）

这是一个用于学习 **注册表单自动化测试技术** 的安全演示项目。

> 重要说明：本仓库不包含真实账号、一次性验证数据、临时邮箱接收逻辑、规模化账号创建逻辑或任何第三方服务的绕过代码。请仅在你拥有授权的测试环境、自己的产品或本地演示页面中使用。

## 项目目标

- 演示如何使用 Playwright 自动填写注册表单
- 演示如何设计可配置的表单字段映射
- 演示如何做基本的自动化测试日志记录
- 演示公开仓库前如何排除敏感数据

## 核心技术文档

- [Core Techniques for Authorized Form Automation Testing](docs/core-techniques.md)

## 不包含的内容

- 不包含任何真实邮箱、密码或账号数据
- 不包含一次性验证数据接收或临时邮箱 API 调用
- 不包含规模化注册、持续注册、并发账号创建功能
- 不包含目标网站的专用选择器或规避检测逻辑
- 不包含本机路径、LaunchAgent、日志、浏览器缓存或虚拟环境

## 目录结构

```text
.
├── README.md
├── SECURITY.md
├── PUBLICATION_AUDIT.md
├── requirements.txt
├── examples
│   ├── demo_form.html
│   └── sample_config.json
└── src
    ├── config_loader.py
    ├── fake_verification.py
    ├── form_automation_demo.py
    ├── models.py
    └── runner.py
```

## 快速开始

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python src/form_automation_demo.py --config examples/sample_config.json
```

脚本默认打开本地演示页面 `examples/demo_form.html`，填写示例数据并输出执行日志。

## 合规使用

你应该只在以下场景使用本项目：

- 自己产品的注册流程回归测试
- 本地或测试环境中的表单自动化学习
- 获得明确授权的 QA / E2E 测试

请不要将本项目用于垃圾注册、绕过服务限制、规避付费、薅羊毛或违反任何网站服务条款的行为。
