---
name: shanghai-intelligence-curation
description: 从上海本地宝、市政府、16区机关和公共机构发现、核验和发布上海本地七大专题城市情报，生成可审计的事件卡和 Olah-style 深度 HTML 报告。
---

# 上海城市情报采编 Skill

适用时机：上海地区的政策、招聘与编制、住房与落户、补贴福利、教育考试、城市经济、交通民生、活动生活情报更新。

## 入口
先阅读项目根目录 AGENTS.md、config/topics.json、config/districts.json 和 config/sources.json。需要长文可视化时，进一步使用 .pi/skills/olah-style-paper-posts/SKILL.md 与 references/，不可将论文公式验证的要求机械应用到政策；应改为核对正式文件条文、版本、部门、日期和量化指标。

## 阶段
0. 寻找线索：本地宝 + 官方政策/公告，保留原始 URL、首次观察时间及发布日期。
1. 查重：以官方文件文号、事件关键人群与内容指纹、既存事件 ID 归并；关联不同发布版本。
2. 核验：优先主管部门、区政府、公告发布单位、办事服务；核对资格、金额、编制性质、时间、截止条件。
3. 结构化：按照 data/events/example.json 生成事件；没有可复核的官方依据只能标记 draft。
4. 分析：单条情报说明为什么重要、谁受影响、什么已确定、哪些尚未发布、应采取的操作。
5. 深度研究：高价值议题依据原始文件绘制独立 SVG、时间线、决策树，单图回答单个问题，每条关键主张对应 evidence.json。
6. 质量与发布：python scripts/validate_data.py && python scripts/build_site.py && python -m unittest discover -s tests -v；检查输出并提交 PR。合并后核对 Actions 状态与 Pages 实际可访问性。

## 分类
jobs / housing / benefits / education / economy / mobility / lifestyle。主题名称和说明始终从 config/topics.json 获取，不写死第二套。
