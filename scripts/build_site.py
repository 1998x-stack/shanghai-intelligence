#!/usr/bin/env python3
"""Build the GitHub Pages site from audited JSON records. Python stdlib only."""
from __future__ import annotations

import html
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
BASE = os.getenv("SITE_BASE", "/shanghai-intelligence/").strip()
BASE = "/" + BASE.strip("/") + "/" if BASE.strip("/") else "/"
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOPICS = json.loads((ROOT / "config/topics.json").read_text(encoding="utf-8"))
DISTRICTS = json.loads((ROOT / "config/districts.json").read_text(encoding="utf-8"))
SOURCES = json.loads((ROOT / "config/sources.json").read_text(encoding="utf-8"))
REPORTS = json.loads((ROOT / "config/reports.json").read_text(encoding="utf-8"))
TOPIC_BY_ID = {x["id"]: x for x in TOPICS}
DISTRICT_BY_ID = {x["id"]: x for x in DISTRICTS}


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def local(path: str = "") -> str:
    return BASE + path.lstrip("/")


def official_url(value: str) -> str:
    parsed = urlparse(value or "")
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("Only absolute HTTPS source URLs are accepted")
    return esc(value)


def write(path: str, content: str) -> None:
    dest = OUT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")


def valid_day(value: str) -> bool:
    try:
        return date.fromisoformat(value).isoformat() == value
    except (TypeError, ValueError):
        return False


def load_events() -> list[dict]:
    events = []
    ids = set()
    for path in sorted((ROOT / "data/events").glob("*.json")):
        item = json.loads(path.read_text(encoding="utf-8"))
        event_id = item.get("id", "")
        if not ID_RE.fullmatch(event_id):
            raise ValueError(f"{path}: invalid stable id")
        if event_id in ids:
            raise ValueError(f"{path}: duplicate event id {event_id}")
        ids.add(event_id)
        if item.get("topic") not in TOPIC_BY_ID:
            raise ValueError(f"{path}: unknown topic")
        if not valid_day(item.get("published_at", "")):
            raise ValueError(f"{path}: invalid published_at")
        if item.get("deadline") and not valid_day(item["deadline"]):
            raise ValueError(f"{path}: invalid deadline")
        if not isinstance(item.get("districts", []), list) or any(
            x not in DISTRICT_BY_ID for x in item.get("districts", [])
        ):
            raise ValueError(f"{path}: unknown district")
        if item.get("status") not in ("draft", "verified"):
            raise ValueError(f"{path}: status must be draft or verified")
        if not item.get("title") or not item.get("summary"):
            raise ValueError(f"{path}: title and summary required")
        if item["status"] == "verified":
            for key in ("official_url", "source_url"):
                official_url(item.get(key, ""))
            if not valid_day(item.get("checked_at", "")):
                raise ValueError(f"{path}: verified event missing valid checked_at")
            claims = item.get("evidence")
            if not isinstance(claims, list) or len(claims) == 0:
                raise ValueError(f"{path}: verified event needs claim-level evidence")
            for claim in claims:
                if not claim.get("claim") or not claim.get("locator"):
                    raise ValueError(f"{path}: evidence requires claim and locator")
                if claim.get("status") != "verified":
                    raise ValueError(f"{path}: unpublished evidence in verified event")
                official_url(claim.get("source_url", ""))
            events.append(item)
    return sorted(events, key=lambda e: (e["published_at"], e["id"]), reverse=True)


def badge(text: str, cls: str = "") -> str:
    return f'<span class="badge {cls}">{esc(text)}</span>'


def nav_item(path: str, name: str, current: str) -> str:
    cls = ' class="active"' if current == name else ""
    return f'<a{cls} href="{local(path)}">{esc(name)}</a>'


def layout(title: str, body: str, current: str = "", description: str = "") -> str:
    nav = "".join((
        nav_item("", "首页", current),
        nav_item("daily/", "每日简报", current),
        nav_item("monthly/", "月度档案", current),
        nav_item("topics/", "专题", current),
        nav_item("districts/", "地区", current),
        nav_item("archive/", "档案", current),
        nav_item("reports/", "深度研究", current),
        nav_item("sources/", "来源", current),
    ))
    desc = description or "上海政策、就业、住房、教育、经济、民生与活动情报"
    return f"""<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#122638">
<meta name="description" content="{esc(desc)}">
<title>{esc(title)} | Shanghai Intelligence</title>
<link rel="stylesheet" href="{local('assets/site.css')}">
<script defer src="{local('assets/site.js')}"></script>
</head><body>
<a class="skip-link" href="#main">跳转至正文</a>
<header class="site-header"><div class="header-inner">
<a class="brand" href="{local('')}"><span class="brand-mark">沪</span><span>SHANGHAI <b>INTELLIGENCE</b><small>上海城市情报档案</small></span></a>
<nav aria-label="主导航">{nav}</nav></div></header>
<main id="main">{body}</main>
<footer><div class="shell footer-grid"><div><strong>Shanghai Intelligence</strong><p>来自公开信息的独立研究项目，并非上海市政府官方网站。</p></div>
<div><a href="{local('sources/')}">数据来源与核验规则</a><p>重要事项请以官方原文及办理系统为准。</p></div></div></footer>
</body></html>"""


def section_head(kicker: str, title: str, sub: str = "") -> str:
    return (f'<div class="section-title"><span class="eyebrow">{esc(kicker)}</span>'
            f'<h2>{esc(title)}</h2><p>{esc(sub)}</p></div>')


def event_card(e: dict) -> str:
    topic = TOPIC_BY_ID[e["topic"]]
    district = " / ".join(DISTRICT_BY_ID[d]["name"] for d in e.get("districts", [])) or "全市"
    deadline = f' · 截止 {esc(e["deadline"])}' if e.get("deadline") else ""
    return f"""<article class="event-card" data-search="{esc(e["title"] + ' ' + e["summary"] + ' ' + topic["name"] + ' ' + district)}">
    <div class="card-meta"><span>{esc(e["published_at"])}</span>{badge(topic["name"])}<span>{esc(district)}{deadline}</span></div>
    <h3><a href="{local('events/' + e['id'] + '/')}">{esc(e["title"])}</a></h3>
    <p>{esc(e["summary"])}</p><a class="read-more" href="{local('events/' + e['id'] + '/')}">查看证据与行动建议 <span aria-hidden="true">↗</span></a>
    </article>"""


def event_cards(items: list[dict], none: str = "暂无通过官方核验的情报；待核实线索不会自动公开。") -> str:
    return "".join(event_card(x) for x in items) if items else f'<div class="empty-state"><strong>暂无已核验事件</strong><p>{esc(none)}</p></div>'


def hero(kicker: str, title: str, sub: str, dark: bool = False) -> str:
    cls = " hero-dark" if dark else ""
    return f'<section class="hero{cls}"><div class="shell"><span class="eyebrow">{esc(kicker)}</span><h1>{esc(title)}</h1><p>{esc(sub)}</p></div></section>'


def build_home(events: list[dict]) -> None:
    stats = f"""<div class="stat-row">
    <div><strong>{len(events)}</strong><span>已核验情报</span></div>
    <div><strong>{len(TOPICS)}</strong><span>长期监测专题</span></div>
    <div><strong>{len(DISTRICTS)}</strong><span>行政区观察范围</span></div>
    </div>"""
    topic_cards = "".join(
        f'<a class="topic-card" href="{local("topics/"+t["id"]+"/")}"><span class="small-index">专题 {i:02}</span>'
        f'<h3>{esc(t["name"])}</h3><p>{esc(t["description"])}</p>'
        f'<span class="topic-foot">{esc(t["analysis"])} <span aria-hidden="true">↗</span></span></a>'
        for i, t in enumerate(TOPICS, 1)
    )
    latest = event_cards(events[:8])
    body = (hero("CITY SIGNALS · 城市观察", "看清上海的政策、机会与变化。",
                 "从本地资讯发现线索，以政府及公共机构的一手文件核实，并将每项变化转化为可追溯的行动情报。", True)
            + f'<div class="shell">{stats}</div>'
            + '<section class="shell section">' + section_head("01 / FIELD NOTES", "最新核心情报", "只展示已建立官方证据链的事件，不以转载数量作为质量指标。")
            + f'<div class="event-list">{latest}</div></section>'
            + '<section class="shell section">' + section_head("02 / SEVEN DESKS", "七大长期专题", "每个主题拥有独立的历史档案、来源与新增事件入口。")
            + f'<div class="topic-grid">{topic_cards}</div></section>'
            + '<section class="shell section two-columns"><div>' + section_head("03 / HOW IT WORKS", "每条情报都可以追溯", "发现线索 → 核实原文 → 关联版本 → 判断适用人群 → 提炼行动。")
            + f'<a class="text-link" href="{local("sources/")}">查看来源目录和核验要求 →</a></div>'
            + '<div class="method-box"><span class="badge">核验原则</span><ol><li>本地宝只作发现入口</li><li>以主管部门正式原文为准</li><li>区分发布日期与实施日期</li><li>明确资格、期限和操作入口</li></ol></div></section>')
    write("index.html", layout("首页", body, "首页"))


def build_topics(events: list[dict]) -> None:
    cards = "".join(
        f'<a class="topic-card" href="{local("topics/"+t["id"]+"/")}"><span class="small-index">TRACK {i:02}</span>'
        f'<h3>{esc(t["name"])}</h3><p>{esc(t["description"])}</p><span class="topic-foot">进入专题 →</span></a>'
        for i, t in enumerate(TOPICS, 1))
    write("topics/index.html", layout("七大专题", hero("TOPIC DIRECTORY", "七大情报专题", "按领域持续积累，不因每天更新而丢失历史。")
          + f'<section class="shell section topic-grid">{cards}</section>', "专题"))
    for t in TOPICS:
        items = [e for e in events if e["topic"] == t["id"]]
        watch = "".join(badge(w) for w in t["watch"])
        body = (hero("TRACK / " + t["id"].upper(), t["name"], t["description"])
                + f'<div class="shell section"><div class="topic-intro"><div><h2>监测范围</h2><div class="badge-row">{watch}</div></div>'
                + f'<div><h2>核心分析</h2><p>{esc(t["analysis"])}</p></div></div>'
                + section_head("LATEST", "已核验事件", f"本专题累计 {len(items)} 条公开事件。")
                + f'<div class="event-list">{event_cards(items)}</div></div>')
        write(f'topics/{t["id"]}/index.html', layout(t["name"], body, "专题"))


def build_districts(events: list[dict]) -> None:
    links = "".join(
        f'<a class="district-link" href="{local("districts/"+d["id"]+"/")}"><span>{esc(d["name"])}</span><span>↗</span></a>'
        for d in DISTRICTS)
    write("districts/index.html", layout("16区观察", hero("DISTRICT WATCH", "上海16区观察", "区级招聘、资金申报、教育事项与地方实施细则。")
          + f'<section class="shell section"><div class="district-grid">{links}</div></section>', "地区"))
    for d in DISTRICTS:
        items = [e for e in events if d["id"] in e.get("districts", [])]
        body = hero("DISTRICT / SHANGHAI", d["name"], "关注区政府、相关部门及公共机构发布的正式事项。")
        body += '<section class="shell section">' + section_head("LOCAL SIGNALS", "本区事件", f"已核验 {len(items)} 条") + event_cards(items) + '</section>'
        write(f'districts/{d["id"]}/index.html', layout(d["name"], body, "地区"))


def build_archive(events: list[dict]) -> None:
    body = hero("EVENT ARCHIVE", "情报档案", "按关键词、时间、专题与地区定位既往已核实情报。")
    body += ('<section class="shell section">'
             '<label class="search-label" for="archive-search">检索已核验情报</label>'
             '<input id="archive-search" type="search" placeholder="输入政策、机构、地区、关键词…" autocomplete="off">'
             '<p class="search-result" id="search-result" aria-live="polite"></p>'
             '<div class="event-list" id="searchable-events">' + event_cards(events) + '</div></section>')
    write("archive/index.html", layout("情报档案", body, "档案"))


def build_daily(events: list[dict]) -> None:
    by_day = defaultdict(list)
    for e in events:
        by_day[e["published_at"]].append(e)
    days = sorted(by_day, reverse=True)
    links = "".join(
        f'<a class="daily-row" href="{local("daily/"+d+"/")}"><span>{esc(d)}</span><span>{len(by_day[d])} 条已核验情报 ↗</span></a>'
        for d in days)
    if not links:
        links = '<div class="empty-state"><strong>尚无发布日报</strong><p>未来每次新增已核验事件，会自动生成对应日期的档案。</p></div>'
    body = hero("DAILY BRIEFINGS", "每日简报", "按事件原始发布日期汇总，日期不等同于采集时间。")
    body += f'<section class="shell section">{links}</section>'
    write("daily/index.html", layout("每日简报", body, "每日简报"))
    for d in days:
        content = hero("DAILY / " + d, d + " · 上海情报", "以下为这一天发布、已经过官方核验的情报。")
        content += '<section class="shell section">' + event_cards(by_day[d]) + '</section>'
        write(f"daily/{d}/index.html", layout(d + " 日报", content, "每日简报"))



def build_monthly(events: list[dict]) -> None:
    """Evergreen month archives built automatically from published event dates."""
    by_month = defaultdict(list)
    for event in events:
        by_month[event["published_at"][:7]].append(event)
    months = sorted(by_month, reverse=True)
    links = "".join(
        f'<a class="daily-row" href="{local("monthly/" + m + "/")}"><span>{esc(m)}</span><span>{len(by_month[m])} 条已核验情报 ↗</span></a>'
        for m in months)
    if not links:
        links = '<div class="empty-state"><strong>尚无月度档案</strong><p>未来新增经过核验的事件，会按官方发布日期自动归档。</p></div>'
    index = hero("MONTHLY REVIEW", "月度情报档案", "按官方公开发布日期组织，每个月保留独立页面，数据增加后自动更新。")
    index += '<section class="shell section">' + links + '</section>'
    write("monthly/index.html", layout("月度档案", index, "月度档案"))
    for m in months:
        items = by_month[m]
        counts = Counter(e["topic"] for e in items)
        tags = "".join(
            f'<a class="badge" href="{local("topics/" + t["id"] + "/")}">{esc(t["name"])} {counts[t["id"]]}</a> '
            for t in TOPICS if counts.get(t["id"]))
        content = hero("MONTH / " + m, m + " · 上海城市情报", "以下事件以原始官方发布时间归档；不是上海本地宝全站该月报道数量。")
        content += '<section class="shell section"><div class="badge-row">' + tags + '</div>'
        if m == "2026-10":
            content += ('<p><a class="text-link" href="' + local("reports/october-2026-shanghai-intelligence/")
                        + '">阅读2026年10月可视化情报分析 →</a></p>')
        content += '<div class="event-list">' + event_cards(items) + '</div></section>'
        write(f"monthly/{m}/index.html", layout(m + " 月度情报", content, "月度档案"))


def build_events(events: list[dict]) -> None:
    for e in events:
        district = " / ".join(DISTRICT_BY_ID[d]["name"] for d in e.get("districts", [])) or "全市"
        facts = [
            ("所属领域", TOPIC_BY_ID[e["topic"]]["name"]),
            ("地域", district),
            ("官方发布日期", e["published_at"]),
            ("首次观察", e.get("observed_at") or "未记录"),
            ("生效时间", e.get("effective_at") or "尚不明确"),
            ("截止日期", e.get("deadline") or "未设定或尚未确认"),
            ("最后核验", e["checked_at"]),
        ]
        rows = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in facts)
        evid = "".join(
            f'<li><p>{esc(c["claim"])}</p><span>定位：{esc(c["locator"])}</span> '
            f'<a href="{official_url(c["source_url"])}" target="_blank" rel="noopener noreferrer">查看证据 ↗</a></li>'
            for c in e["evidence"]
        )
        body = hero("VERIFIED INTELLIGENCE", e["title"], e["summary"])
        body += (f'<section class="shell section article-layout"><article class="article-body"><h2>关键信息</h2><p>{esc(e["summary"])}</p>'
                 f'<h2>涉及对象与影响</h2><p>{esc(e.get("impact") or "以官方文件适用条件为准。")}</p>'
                 f'<h2>可以采取的行动</h2><p>{esc(e.get("action") or "阅读最新官方原文并核对适用条件。")}</p>'
                 f'<h2>证据账本</h2><ol class="evidence-list">{evid}</ol>'
                 f'<p><a href="{official_url(e["official_url"])}" target="_blank" rel="noopener noreferrer">阅读官方原文 ↗</a></p>'
                 f'<p><a href="{official_url(e["source_url"])}" target="_blank" rel="noopener noreferrer">最初线索来源 ↗</a></p></article>'
                 f'<aside class="detail-panel"><h3>记录元数据</h3><dl>{rows}</dl>{badge("已核验", "verified")}'
                 f'<p>本页是独立整理的公开信息摘要，法律及办理效力以主管部门正式文件为准。</p></aside></section>')
        write(f'events/{e["id"]}/index.html', layout(e["title"], body, "档案", e["summary"]))


def build_sources() -> None:
    cards = "".join(
        f'<article class="source-card">{badge("一手官方" if s["type"] == "official" else "二次发现")}'
        f'<h3>{esc(s["name"])}</h3><p>{esc("关联专题：" + "、".join(TOPIC_BY_ID[t]["name"] for t in s["topics"]))}</p>'
        f'<a href="{official_url(s["url"])}" target="_blank" rel="noopener noreferrer">访问来源 ↗</a></article>'
        for s in SOURCES)
    body = hero("EVIDENCE LIBRARY", "来源与证据", "所有发布内容以可公开访问、能定位的证据为基础。")
    body += ('<section class="shell section">' + section_head("SOURCE REGISTER", "数据源目录", "官方来源与二次线索明确区分。")
             + f'<div class="source-grid">{cards}</div></section>'
             '<section class="shell section narrow"><h2>核验规则</h2><p>本地宝等二次来源用于发现信息；法律、行政程序、资格、岗位身份、金额和时间，以主管部门公布的原文及办理系统为准。</p>'
             '<p>征求意见、会议原则通过、正式颁布、生效、修订和废止必须分别标识。没有确切证据时不得推断适用资格。</p></section>')
    write("sources/index.html", layout("来源与证据", body, "来源"))


def build_reports() -> None:
    cards = []
    for r in REPORTS:
        slug = r.get("slug", "")
        if not ID_RE.fullmatch(slug) or r.get("topic") not in TOPIC_BY_ID:
            raise ValueError("Invalid report catalog entry")
        folder = ROOT / "content/reports" / slug
        if not (folder / "index.html").exists() or not (folder / "evidence.json").exists():
            raise ValueError(f"Report {slug} must contain index.html and evidence.json")
        shutil.copytree(folder, OUT / "reports" / slug, dirs_exist_ok=True)
        cards.append(f'<article class="event-card">{badge(TOPIC_BY_ID[r["topic"]]["name"])}'
                     f'<h3><a href="{local("reports/"+slug+"/")}">{esc(r["title"])}</a></h3>'
                     f'<p>{esc(r.get("summary", ""))}</p><span class="card-meta">{esc(r.get("published_at",""))}</span></article>')
    body = hero("DEEP RESEARCH", "深度研究", "运用可交互图解、政策版本比较与逐条引用，把复杂规定解释清楚。")
    body += '<section class="shell section">' + (''.join(cards) if cards else '<div class="empty-state"><strong>专题长文持续建设中</strong><p>研究通过证据审查和浏览器 QA 后，会自动出现在这里。</p></div>') + '</section>'
    write("reports/index.html", layout("深度研究", body, "深度研究"))


def build() -> None:
    events = load_events()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "assets").mkdir()
    shutil.copy2(ROOT / "assets/site.css", OUT / "assets/site.css")
    shutil.copy2(ROOT / "assets/site.js", OUT / "assets/site.js")
    write(".nojekyll", "")
    build_home(events)
    build_topics(events)
    build_districts(events)
    build_archive(events)
    build_daily(events)
    build_monthly(events)
    build_events(events)
    build_sources()
    build_reports()
    write("404.html", layout("页面不存在", hero("404", "未找到此页面", "请通过主页重新进入专题或档案。")
                             + f'<section class="shell section"><a href="{local("")}">返回首页 ↗</a></section>'))
    write("feed.json", json.dumps([{
        "id": e["id"], "title": e["title"], "topic": e["topic"], "published_at": e["published_at"],
        "summary": e["summary"], "url": local("events/" + e["id"] + "/")
    } for e in events], ensure_ascii=False, indent=2) + "\n")
    print(f"Built {_count_files()} files, {len(events)} verified events, {len(TOPICS)} topics, {len(DISTRICTS)} districts; base={BASE}")


def _count_files() -> int:
    return sum(f.is_file() for f in OUT.rglob("*"))


if __name__ == "__main__":
    build()
