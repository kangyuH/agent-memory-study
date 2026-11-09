"""Parse and scope a technical course outline without model inference."""

import hashlib
import re
from pathlib import Path


class WorkflowError(ValueError):
    """A problem that must be resolved before the workflow can continue."""


EP_ID = r"EP\d{2,}"
EP_HEADING = re.compile(rf"^###\s+({EP_ID})\s*(?:[｜|:：—–-]\s*|\s+)(\S.*)$", re.I)
EP_MARKER = re.compile(rf"^#{{1,6}}\s+{EP_ID}\b", re.I)
SECTION = re.compile(r"^##\s+(.+?)\s*$")
DEPENDENCIES = re.compile(r"跨章节知识依赖|跨期依赖|^dependencies$|^episode dependencies$", re.I)
EP_CHAIN = re.compile(rf"{EP_ID}(?:\s*(?:→|->)\s*{EP_ID})+", re.I)
EP_RANGE = re.compile(rf"({EP_ID})\s*(?:\.\.|[—–~-])\s*({EP_ID})", re.I)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
BULLET = re.compile(r"^\s*-\s+")
STRUCTURED = {
    "question": ("主问题", "核心问题", "研究问题", "question", "core question"),
    "context": ("历史现场与约束", "前沿问题与约束", "背景与约束", "context", "constraints"),
    "mechanisms": ("尝试与技术机制", "技术路线", "机制", "mechanisms", "approaches"),
    "tradeoffs": ("有效与局限", "局限与取舍", "trade-offs", "tradeoffs", "limitations"),
    "next_question": ("导向新问题", "新问题", "最终开放问题", "next question"),
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def visible_lines(lines):
    fence = None
    for number, line in enumerate(lines, 1):
        match = FENCE.match(line)
        if match:
            marker, tail = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not tail.strip():
                fence = None
            continue
        if fence is None:
            yield number, line


def fields(lines, start, end):
    result = {}
    for _, line in visible_lines(lines[start - 1:end]):
        match = re.match(r"^\s*[-*]\s+\*\*(.+?)\*\*\s*[：:]\s*(.+)$", line)
        if not match:
            continue
        label, value = match.groups()
        for field, aliases in STRUCTURED.items():
            if label.lower() in aliases:
                if field in result:
                    raise WorkflowError(f"第 {start} 行之后的 {label} 出现多次")
                result[field] = value.strip()
    return result


def parse_outline(path, *, expected_episodes=None, expected_topics=None):
    path = Path(path)
    data = path.read_bytes()
    lines = data.decode("utf-8-sig").splitlines()
    episodes = {}
    topics = {}
    chains = []
    topic = None
    episode = None
    dependency_section = False

    for number, line in visible_lines(lines):
        section = SECTION.match(line)
        heading = EP_HEADING.match(line)
        if section or heading:
            if episode:
                episodes[episode]["end"] = number - 1
                episode = None
        if section:
            topic = section[1]
            dependency_section = bool(DEPENDENCIES.search(topic))
        elif heading:
            episode = heading[1].upper()
            if not topic or dependency_section or episode in episodes:
                raise WorkflowError(f"第 {number} 行的 {episode} 主题无效或编号重复")
            episodes[episode] = {
                "title": heading[2].strip(), "topic": topic, "start": number, "end": len(lines),
                "prerequisites": [],
            }
            topics.setdefault(topic, []).append(episode)
        elif EP_MARKER.match(line):
            raise WorkflowError(f"第 {number} 行不是可识别的分期标题。请用 ### EPnn｜标题")
        elif dependency_section and BULLET.match(line):
            matches = EP_CHAIN.findall(line)
            if re.search(EP_ID, EP_CHAIN.sub("", line), re.I):
                raise WorkflowError(f"第 {number} 行的依赖无法解析。请用 EP01 → EP02")
            for chain in matches:
                chains.append(re.findall(EP_ID, chain.upper()))

    if not episodes:
        raise WorkflowError("未发现分期。请使用 ## 主题和 ### EPnn｜标题")
    for label, found, target in (("期数", len(episodes), expected_episodes), ("主题数", len(topics), expected_topics)):
        if target is not None and found != target:
            raise WorkflowError(f"{label}与预期不符。发现 {found}，预期 {target}")
    actual = list(episodes)
    expected = [f"EP{i:02}" for i in range(1, len(actual) + 1)]
    if actual != expected:
        raise WorkflowError(f"期数须从 EP01 连续递增。实际编号为 {', '.join(actual)}")

    for chain in chains:
        for upstream, downstream in zip(chain, chain[1:]):
            if upstream not in episodes or downstream not in episodes:
                raise WorkflowError(f"依赖引用未知期数 {upstream} → {downstream}")
            prerequisites = episodes[downstream]["prerequisites"]
            if upstream not in prerequisites:
                prerequisites.append(upstream)

    for episode, item in episodes.items():
        details = fields(lines, item["start"], item["end"])
        item["fields"] = details
        item["question"] = details.get("question", item["title"])

    result = {
        "outline": str(path.resolve()), "outline_sha256": hashlib.sha256(data).hexdigest(),
        "topics": topics, "episodes": episodes,
    }
    ordered(result, actual)
    return result


def ordered(index, selected, include_prerequisites=True):
    result = []
    visited = set()
    visiting = set()
    selected = set(selected)

    def visit(episode):
        if episode in visiting:
            raise WorkflowError(f"章节依赖成环，涉及 {episode}")
        if episode in visited:
            return
        visiting.add(episode)
        for prerequisite in index["episodes"][episode]["prerequisites"]:
            if include_prerequisites or prerequisite in selected:
                visit(prerequisite)
        visiting.remove(episode)
        visited.add(episode)
        result.append(episode)

    for episode in index["episodes"]:
        if episode in selected:
            visit(episode)
    return result


def select(index, expression):
    episodes = list(index["episodes"])
    normalized = expression.strip().upper()
    if normalized in index["episodes"]:
        return [normalized]
    if match := EP_RANGE.fullmatch(normalized):
        first, last = match.groups()
        if first in episodes and last in episodes and episodes.index(first) <= episodes.index(last):
            return episodes[episodes.index(first):episodes.index(last) + 1]
    if expression in index["topics"]:
        return index["topics"][expression]
    raise WorkflowError(f"无效选择 {expression!r}。可用单期、EP01..EP04 或索引中的完整主题名")


def scope(index, episode):
    entries = index["episodes"]
    item = entries[episode]
    content = Path(index["outline"]).read_bytes()
    if hashlib.sha256(content).hexdigest() != index["outline_sha256"]:
        raise WorkflowError("课程大纲在读取过程中发生变化，请重跑")
    lines = content.decode("utf-8-sig").splitlines()
    ids = list(entries)
    position = ids.index(episode)

    def summary(key):
        return {"episode": key, **entries[key]}

    return {
        "episode": episode, "outline_sha256": index["outline_sha256"],
        "entry": summary(episode),
        "section": "\n".join(lines[item["start"] - 1:item["end"]]).rstrip(),
        "prerequisites": [summary(key) for key in item["prerequisites"]],
        "neighbors": [summary(key) for key in ids[max(0, position - 1):position + 2] if key != episode],
    }
