# Olah-style Posts

**面向论文深度解读的工程化写作 Skill：把科学证据变成可验证、可交互、可阅读的技术长文。**

受 Christopher Olah《Understanding LSTM Networks》的渐进式图解方法，以及 Harvard NLP《The Annotated Transformer》的逐段可执行实现方法启发。本项目提取的是**教学设计与工程工作流**，不是搬运上述作品的文字、代码或图片。

[![Validate](https://github.com/1998x-stack/Olah-style-posts/actions/workflows/validate.yml/badge.svg)](https://github.com/1998x-stack/Olah-style-posts/actions/workflows/validate.yml)

## 设计原则

**科学正确性 > 因果叙事 > 信息图可读性 > 工程可复现 > 视觉装饰。** 每篇文章从读者的具体困惑开始，把一个复杂模型拆成有状态的 SVG 示意图，用符号/形状重建计算路径，再以可运行的代码和论文表格核验。论文主张、教学简化、代码实现以及现代扩展必须明确分开。

## 快速入口

| 资源 | 用途 |
|---|---|
| [`SKILL.md`](skills/olah-style-paper-posts/SKILL.md) | Agent 使用说明、七阶段工作流和验收门槛 |
| [`references/`](skills/olah-style-paper-posts/references/) | 叙事、论文拆解、引用、CSS、SVG、交互、浏览器 QA 和质量评分 |
| [`math-typesetting.md`](skills/olah-style-paper-posts/references/math-typesetting.md) | 数学公式：离线 MathML、分式/求和/脚本、移动端滚动及静态与浏览器验证 |
| [`assets/`](skills/olah-style-paper-posts/assets/) | HTML 模板、CSS 设计系统、JavaScript 增强与 SVG 图元 |
| [`scripts/`](skills/olah-style-paper-posts/scripts/) | 新建文章、静态校验、浏览器 QA、带计算样式的 SVG 提取 |
| [`examples/resnet/`](examples/resnet/index.html) | ResNet：11 章，10 幅独立 SVG，残差/梯度/投影/实验对照 |
| [`examples/transformer/`](examples/transformer/index.html) | Transformer：16 章，13 幅独立 SVG，交互 QKV/Mask/Encoder–Decoder |
| [`tests/`](tests/) | 禁止无关小字、基本结构与独立 SVG 解析回归测试 |

## 仓库结构

```text
.
├── README.md
├── AGENTS.md
├── requirements-dev.txt
├── .github/workflows/validate.yml
├── index.html                      # 示例入口（可作 Pages 根目录）
├── docs/index.html                 # 同一入口的本地版本
├── examples/
│   ├── resnet/
│   │   ├── index.html
│   │   ├── evidence.json
│   │   └── assets/*.svg
│   └── transformer/
│       ├── index.html
│       ├── evidence.json
│       ├── mini_attention.py
│       └── assets/*.svg
├── skills/olah-style-paper-posts/
│   ├── SKILL.md
│   ├── assets/css/article.css
│   ├── assets/js/interactions.js
│   ├── assets/templates/article.html
│   ├── references/*.md
│   └── scripts/
│       ├── new_post.py
│       ├── validate.py
│       ├── extract_svg.py
│       └── browser_check.py
└── tests/test_validator.py
```

## 一分钟开始

先安装开发依赖：

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
```

创建文章（在仓库根目录）：

```bash
python skills/olah-style-paper-posts/scripts/new_post.py \
  --slug understanding-mamba --title 'Understanding Mamba' \
  --dek '为什么有选择的状态空间模型能在序列建模中发挥作用？'
```

完成研究与绘图后，验证并导出可独立查看的 SVG：

```bash
python skills/olah-style-paper-posts/scripts/validate.py examples/resnet/index.html
python skills/olah-style-paper-posts/scripts/extract_svg.py examples/resnet/index.html --out /tmp/resnet-svg
python skills/olah-style-paper-posts/scripts/browser_check.py examples/resnet/index.html --output /tmp/resnet-qa
python -m pytest -q
```

浏览器脚本在 1440、768、390、360px 宽度下采集截图、记录页面异常和溢出，并测试至少一个真实交互（当文章存在按钮时）。输出 `report.json`；**只有执行过的检查才算通过**。

## 论文到文章：七道门

| 阶段 | 输入 | 产物 | 不可省略的检查 |
|---|---|---|---|
| 0. 论文取证 | 原始论文/代码 | 版本、主要结果、表格定位 | 指标是否匹配数据集/评价口径 |
| 1. 叙事编排 | 知识难点 | 故事主线、图示脚本 | 一图一问；不先堆公式 |
| 2. 技术校准 | 公式/模型图 | 张量维度、假设、变体边界 | 信息流拓扑完全正确 |
| 3. 页面设计 | 主文稿 | 语义 HTML、统一 CSS | 无移动端溢出、支持打印 |
| 4. SVG 工程 | 图示脚本 | 原始 SVG + 可提取 SVG | 字体/箭头/label 可独立渲染 |
| 5. 可运行解读 | 精简算法 | Python 代码 + 形状/数值测试 | 测试有真实断言 |
| 6. 浏览器验收 | 完成页面 | 截图、错误日志和 QA JSON | 实际 Chromium + 控件交互 |
| 7. 发布归档 | 验证产物 | ZIP/PR/发布版本 | 远端文件可核验 |

## 示例：两篇文章如何复用同一个 Skill？

**ResNet**：从“层数增加反而训练误差升高”提出问题，进而解释残差映射、跳跃连接、反向传播、Basic/Bottleneck Block、投影捷径及实验对照。原始论文：[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)。

**Transformer**：从 LSTM 的顺序计算限制出发，解释 Q/K/V 的角色、注意力得分与 Softmax、Mask、多头组合、位置编码、完整 Encoder–Decoder，并对照代码构建可交互演示。原始论文：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)。示例 PyTorch 代码是最小注意力单元，**不是**完整机器翻译复现。

## 文章风格与制作边界

- 正文仅呈现与研究主题相关的内容。不要把“原创图解”“单文件离线 HTML”“参考某某风格”“浏览器打印适配”之类生产元信息写在文章首尾。
- 图示独立绘制，不复制 Colah 或 Annotated Transformer 的原图、原文、原代码；尊重第三方素材的许可。
- 文章自身应能离线阅读；默认不加载 CDN、外部字体、遥测服务或客户端依赖。
- 关键数学公式采用真实的数学结构（默认浏览器原生 MathML），不要用 Unicode 字符串拼凑复杂公式；必须检查 SVG 数学标签边界、无障碍语义、手机宽度和离线环境。
- 任何实验图表附来源定位，推导值必须标注为计算结果，教学示例不能伪装为论文复现。
- README、Skill 文档和 QA 报告可以记录制作过程；文章正文不应记录。

## 参考资料

1. Christopher Olah, [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/), 2015.
2. Harvard NLP, [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/), updated 2022.
3. He et al., [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385), 2015/2016.
4. Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), 2017.

### 署名与许可说明

本项目的文章和图像是独立编写与绘制的教学产物。上述外部内容仅作为引用与方法论参考；未附加经核验的开源许可证，因此不要默认将其或第三方资源归入某种特定授权。若准备将本项目进一步开放再利用，请先在仓库中明确适用许可证和贡献规则。
