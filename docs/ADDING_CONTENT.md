# 新增情报与报告

## 新增事件
复制 data/events/example.json（这个示例为 draft，默认不公开），换成独一无二的稳定 ID。主题 ID 必须来自 config/topics.json，地区 ID 来自 config/districts.json；全市事项可用空数组。

研究中先保留 draft，收到官方完整原文后逐项核对，写入 official_url、evidence 及 checked_at，再改为 verified。

示例字段：id, title, topic, districts, published_at (YYYY-MM-DD), observed_at, effective_at, deadline, summary, impact, action, source_url, official_url, evidence[], status。

所有事件自动出现在 archive、所属专题、地区、日报（按发布日）、详情页及首页最新事件，无需编辑前端代码。

## 新增深度文章
创建 content/reports/<slug>/index.html（可附 assets/*.svg、evidence.json）；在 config/reports.json 增加 {slug,title,summary,topic,published_at}。
使用 .pi/skills/olah-style-paper-posts/SKILL.md 的长文结构与 QA 流程，但所有政策主张以官方文件为依据。报告内容必须含来源、版本/生效日期、适用边界，且说明分析是事实还是推论。

## 不得违反
- 旧 URL 和稳定事件 ID 不应改变；发生政策修订时通过历史版本或者关联事件标记 superseded。
- 不发布无来源的数值、名额、截止时间、官网链接或编制身份。
- 禁止把本地宝二次转载当作主管部门官方文书。
- 不伪造已执行的测试、已运行的监测、GitHub Pages 已生效。
