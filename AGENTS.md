# Shanghai Intelligence — Agent Operating Contract

## Mission
维护一个持续增长、可审计的上海城市情报站。七大主题来自 config/topics.json。上海本地宝是发现线索的二手来源，上海市/16区部门及公共机构的正式文件是一手依据。不得把本站表现为官方政府网站。

## Repo conventions
- .pi/skills/Olah-style-posts/：上游 Olah-style-posts 的完整不可编辑归档快照；任何更新必须记录上游 SHA、完整性检查、出处。
- .pi/skills/olah-style-paper-posts/：从上游派生的 Pi Agent 可识别原生 Skill 入口，保留原文件和相对引用。
- .pi/skills/shanghai-intelligence-curation/SKILL.md：上海政策情报研究工作流。
- config/topics.json：七大长期专题，新增专题首先修改此配置。
- config/districts.json：16区归属与导航。
- config/sources.json：来源目录，维护 authority、URL、内容类型。
- data/events/*.json：经核验、可发布的结构化事件；每个文件一个事件。draft 仅用于待审核记录。
- content/reports/<slug>/index.html：独立可视化长文，遵循 Olah 风格但必须用上海政策的一手资料取证。
- scripts/build_site.py：生成静态页面，输出 _site/。不得手动修改 _site/，不提交构建结果。
- .github/workflows/pages.yml：质量校验、构建与 GitHub Pages 部署。

## Mandatory research gates
1. 先调查并去重：查事件 ID、官方文件标题/文号、现有历史版本、已发布日报，不重复造文章。
2. 分层取证：本地宝/媒体仅提供线索；政策标准、适用范围、金额、时间、岗位身份，须由正式主管部门文件或官方办事系统核对。
3. 证据账本：每条关键事实记录 claim、source_url、locator、checked_at、status；公开发布必须 verified，不能把待核实标成正式政策。
4. 事件归一化：每事件一个稳定 ID，一个主专题，可有副标签，地区 ID 来自 districts.json。区分 published_at、observed_at、effective_at、deadline。
5. 政策状态：draft / consultation / announced / effective / expired / superseded / cancelled；不要将征求意见稿或听证方案写成正式规定。
6. 行动提炼：谁适用、办什么、需要什么、到哪里办理、何时截止；不适用时明确说明，避免泛化。
7. 发表审核：Python 数据校验通过；移动端 360/390px、桌面 1440px、可访问性、站内链接和引用质量检查。没有执行的测试不能声称通过。
8. 变更安全：先查主干状态；主题分支、PR、最小差异；保护既有文章和相同 ID 的历史版本，提交时附来源与 QA 记录。
9. 发布验收：必须读取 GitHub Actions 运行结果并访问 Pages URL；有代码不代表部署成功，不编造页面状态或指标。
10. 版权：只发布自己的总结与引用/链接，不批量转载本地宝或政府网站整篇内容；遵守各站服务条款和机器人协议。

## Editorial guardrails
- 简体中文；Asia/Shanghai 日期时区；明确发布时间/生效时间/截止时间。
- 数据没有官方确认则 status=draft，不进入公开站点；空事件列表应显示明确的空状态。
- 不做政治人物优劣排名；政策分析分开写事实、已注明来源的解释、推论与不确定性。
- 所有新增内容必须自然出现在首页、专题页、区县页（如有地区）、档案与详情页，无需人工维护导航。
- 每条新报告在 config/reports.json 注册，使用 content/reports/<slug>/index.html 独立静态 HTML，证据文件与报告同目录。
