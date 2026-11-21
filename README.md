# ZhiLin UI Framework

知林的**只读 UI 框架**。本仓库只包含页面壳、基础导入解析和知识卡只读浏览，不是一个可复现的完整产品。

在线预览：<https://henrygeng430.github.io/ZhiLin/>

架构概览（公开版，最小披露）：<https://henrygeng430.github.io/ZhiLin/architecture.html>

## 能做什么

- 导入完整产品导出的私有数据库 JSON
- 查看课程列表
- 查看知识树
- 查看知识卡片、来源和知识关系
- 查看索引表
- 切换浅色 / 深色主题

导入的数据只在浏览器本地解析，不上传服务器。支持 IndexedDB 的浏览器会在本地保留导入结果。

## 不包含什么

本仓库**不包含**：

- 登录、账号、会话或权限系统
- AI 模型、知乎直答或任何联网问答
- 资料解析、建库、知识树生成或增量更新
- 习题生成、作答、判题或复习
- 学习计划、今日安排或计时
- 知识导出、后台任务或任务中心实现
- 管理员后台、额度、配额或用户管理
- 后端服务、数据库、部署脚本或产品文档

所有页面中的相关入口只保留页面壳，并明确标记为未包含。本仓库不能用于复现完整产品。

## 架构说明

本仓库的 `architecture.html` 展示了 COLA Edition 的公开架构：
分层与依赖方向、请求链路、核心切片的职责边界、质量门禁与渐进式迁移策略。
页面只包含框架级说明和示意代码，不包含账号、建库、AI、题库、计划、管理员等业务核心实现。

`cola-skeleton/` 是一个可运行的公开最小后端：领域端口、应用用例、内存/SQLite 适配器、
标准库 HTTP 服务、统一响应包络、CRUD、分页、依赖方向测试和 HTTP 冒烟测试。
示例领域为通用 Note，不包含知林的账号、建库、AI、题库、计划、额度或管理员业务。

```bash
cd cola-skeleton
python server.py --port 8098 --db ./notes.db
PYTHONPATH=. python -m unittest discover -s tests -v
```

## 本地运行

```bash
python -m http.server 8080
```

打开 `http://localhost:8080`。

点击「导入数据库」选择完整产品导出的 JSON 文件；也可以点击「加载示例数据」查看合成示例。示例数据只用于演示页面结构，不是真实课程。

## 目录

```text
index.html              页面入口
assets/app.min.css      构建后的样式
assets/app.min.js       构建后的只读框架
sample-library.json     合成示例数据
LICENSE                 MIT
```

## 许可

MIT License，见 [LICENSE](LICENSE)。
