# Shanghai Intelligence · 上海城市情报

面向上海的七专题公开政策与生活机会情报库：招聘与编制、住房与落户、补贴与福利、教育考试、城市经济、交通与民生、活动与生活。

**站点（部署成功后）：** https://1998x-stack.github.io/shanghai-intelligence/

## 原则
上海本地宝用于发现线索；政府、部门、事业单位和公共机构官网提供核验依据。每条正式事件包含时间、来源、事实、影响对象和行动步骤。未经核验的草稿不进入公开网站。

## 目录
- AGENTS.md：自动化采编、发布与审核契约
- .pi/skills/Olah-style-posts/：上游整仓快照（含示例、QA 截图、脚本）
- .pi/skills/olah-style-paper-posts/：供 Pi Agent 直接加载的原生 Skill
- .pi/skills/shanghai-intelligence-curation/：本项目研究 Skill
- config/：专题、行政区、来源和报告目录
- data/events/：每条事件一个 JSON，可增量扩容
- content/reports/：独立深度 HTML 报告
- scripts/：数据检查和静态站点生成
- _site/：本地生成的部署工件，不提交

## 本地构建
要求 Python 3.11+，不需要 npm。

    python scripts/validate_data.py
    python scripts/build_site.py
    python -m unittest discover -s tests -v
    SITE_BASE=/ python scripts/build_site.py
    python -m http.server 8080 --directory _site

打开 http://localhost:8080/ 查看本地版。GitHub Actions 使用默认 base 路径 /shanghai-intelligence/。

## 增加新内容
1. 阅读 docs/ADDING_CONTENT.md 与 AGENTS.md。
2. 新增 data/events/<stable-id>.json，依据官方来源核验后 status 设 verified。
3. 如果需要可视化长文，新建 content/reports/<slug>/index.html 和 evidence.json，并在 config/reports.json 登记。
4. 运行质量检查，走 PR 合入 main；GitHub Actions 自动构建网站。

## GitHub Pages
使用 .github/workflows/pages.yml；需要在仓库 Settings → Pages 将 Source 设置成 GitHub Actions，并确认 Actions 的 pages/id-token 权限。首次部署以 Actions 的成功状态和公开网页 HTTP 响应为准。

## 上游归档与许可
完整归档来自 https://github.com/1998x-stack/Olah-style-posts，锁定 git tree cd424ad69a66100bfca12e40ec01c44451abae22（共62个文件）。原上游未发现 LICENSE，不能擅自宣称其对第三方采用某种开源许可；沿用原文档中的署名与素材许可注意事项。
