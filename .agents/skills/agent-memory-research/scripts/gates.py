"""Deterministic checks for artifacts. Editorial findings require an independent reviewer."""

import ipaddress
import json
import re
from datetime import date
from urllib.parse import urlsplit, urlunsplit

from outline import WorkflowError, sha256


STAGES = {
    "BRIEF_READY": ("episode_brief.md", "scope_contract.json"),
    "PLAN_READY": ("research_plan.md",),
    "SOURCES_VERIFIED": ("sources.json", "references.md", "retrieval_log.md"),
    "EVIDENCE_BUILT": ("evidence_ledger.json", "evidence_matrix.md", "technical_notes.md", "concepts.json"),
    "RESEARCH_DRAFTED": ("research.md",),
    "RESEARCH_REVIEWED": ("review_research.md", "review_research.json"),
    "PODCAST_DRAFTED": ("podcast_source.md", "notebooklm_source_list.md"),
    "FINAL_REVIEWED": ("review_final.md", "review_final.json"),
    "ACCEPTED": ("acceptance_report.md",),
}
CATEGORIES = {"FACT", "AUTHOR_CLAIM", "EXPERIMENTAL_FINDING", "INFERENCE", "OPEN_QUESTION"}
PRIMARY = {"paper", "code", "official", "primary_replication"}
SCORES = {"facts": 30, "mechanisms": 25, "tradeoffs": 20, "scope": 10, "audio": 10, "traceability": 5}
PROFILES = {"standard-v1": 85, "strict-v1": 92}
HARD_GATES = {
    "sources", "mechanisms", "traceability", "chronology", "failure_modes", "comparison", "scope", "cross_episode",
}
CLAIM_REF = re.compile(r"\[(C\d{2,})\]")
SOURCE_REF = re.compile(r"\[(S\d{2,})\]")
LOCAL_LINK = re.compile(r"(?<!!)\]\((?!https?://|mailto:|#)([^)\s]+)\)", re.I)


def require(condition, message):
    if not condition:
        raise WorkflowError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def records(value, label):
    require(isinstance(value, list) and all(isinstance(row, dict) for row in value),
            f"{label} 应为对象列表")
    return value


def fields(row, names, label):
    for name in names:
        value = row.get(name)
        require(isinstance(value, str) and bool(value.strip()), f"{label} 缺少 {name}")


def strings(value, label, *, nonempty=False):
    require(isinstance(value, list) and all(isinstance(x, str) and x.strip() for x in value)
            and (not nonempty or bool(value)), f"{label} 应为字符串列表")
    return value


def unique(rows, key, pattern):
    result = {}
    for row in rows:
        identifier = row.get(key)
        require(isinstance(identifier, str) and re.fullmatch(pattern, identifier)
                and identifier not in result, f"无效或重复的 {key} {identifier!r}")
        result[identifier] = row
    return result


def iso_date(value, label):
    require(isinstance(value, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)),
            f"{label} 应为 YYYY-MM-DD")
    return date.fromisoformat(value)


def source_date(value, label):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}(?:-\d{2}){0,2}", value),
            f"{label} 日期格式无效")
    parts = value.split("-")
    return iso_date("-".join(parts + ["01"] * (3 - len(parts))), label)


def canonical_url(value):
    url = urlsplit(value)
    host = (url.hostname or "").lower().rstrip(".")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise WorkflowError(f"拒绝来源中的 IP 地址 {value}")
    reserved = {"example.com", "example.org", "example.net"}
    suffixes = {"test", "example", "invalid", "localhost", "local", "internal"}
    require(url.scheme == "https" and bool(re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", host))
            and not any(c.isspace() or ord(c) < 32 for c in value)
            and url.username is None and url.password is None and url.port in (None, 443)
            and host.rsplit(".", 1)[-1] not in suffixes
            and not any(host == name or host.endswith("." + name) for name in reserved),
            f"来源地址必须是有效的公开 HTTPS URL {value}")
    return urlunsplit(("https", host, url.path.rstrip("/"), url.query, ""))


def sources(path, as_of):
    data = unique(records(read_json(path), "sources.json"), "source_id", r"S\d{2,}")
    verified = {}
    seen = set()
    for sid, row in data.items():
        fields(row, ("title", "url", "kind", "status", "checked_on", "note"), sid)
        require(type(row.get("required")) is bool, f"{sid} 缺少布尔字段 required")
        checked = iso_date(row["checked_on"], sid)
        require(row["status"] in {"verified", "unavailable", "rejected"}, f"{sid} 状态无效")
        require(row["kind"] in PRIMARY | {"secondary"}, f"{sid} 来源类型无效")
        if row["status"] != "verified":
            require(not row["required"], f"关键来源 {sid} 未核验，需补证或阻塞")
            continue
        url = canonical_url(row["url"])
        fields(row, ("author", "first_public", "version", "locator"), sid)
        first = source_date(row["first_public"], sid)
        require(first <= iso_date(as_of, "as_of_date") and first <= checked, f"{sid} 时间超出取证边界")
        if row.get("version_date") is not None:
            version_date = source_date(row["version_date"], sid)
            require(first <= version_date <= min(iso_date(as_of, "as_of_date"), checked),
                    f"{sid} 版本时间与取证边界不一致")
        doi = row.get("doi")
        if doi is not None:
            require(isinstance(doi, str) and bool(re.fullmatch(r"10\.\d{4,9}/\S+", doi, re.I)), f"{sid} DOI 格式错误")
        keys = {url, doi.lower()} if doi else {url}
        require(not keys.intersection(seen), f"{sid} 与其他已核验来源重复")
        seen.update(keys)
        verified[sid] = row
    require(any(row["kind"] in PRIMARY for row in verified.values()), "缺少已核验的一手来源")
    return verified


def evidence(path, verified, episode):
    entries = unique(records(read_json(path), "evidence_ledger.json"), "claim_id", r"C\d{2,}")
    require(bool(entries), "证据账本为空")
    for cid, entry in entries.items():
        fields(entry, ("statement", "category", "confidence", "counterevidence", "limitation", "disposition"), cid)
        require(entry.get("episode_id") == episode and entry["category"] in CATEGORIES, f"{cid} 分期或类型错误")
        require(entry["confidence"] in {"high", "medium", "low"}, f"{cid} 置信度无效")
        require(type(entry.get("critical")) is bool, f"{cid} 缺少布尔字段 critical")
        items = records(entry.get("evidence"), cid)
        supported = []
        for item in items:
            fields(item, ("source_id", "locator", "note"), cid)
            sid = item["source_id"]
            require(sid in verified, f"{cid} 引用了未核验或不存在的来源 {sid}")
            require(not item["locator"].startswith(("https://", "http://")), f"{cid} 需要具体章节、页码、表图或代码定位")
            supported.append(verified[sid])
        if entry["critical"] or entry["category"] in {"FACT", "AUTHOR_CLAIM", "EXPERIMENTAL_FINDING"}:
            require(any(row["kind"] in PRIMARY for row in supported), f"{cid} 缺少一手证据")
        if entry["category"] == "EXPERIMENTAL_FINDING":
            require(isinstance(entry.get("experiment"), dict), f"{cid} 缺少实验条件")
            fields(entry["experiment"], ("dataset", "task", "model", "budget", "baseline", "metric", "result",
                                          "significance", "conditions"), cid)
    require(any(row["critical"] for row in entries.values()), "需要标出本期核心主张")
    return entries


def referenced(path, pattern, allowed):
    identifiers = set(pattern.findall(path.read_text(encoding="utf-8")))
    require(bool(identifiers), f"{path.name} 缺少可追溯编号")
    require(identifiers <= set(allowed), f"{path.name} 含未知编号 {', '.join(sorted(identifiers - set(allowed)))}")
    return identifiers


def concepts(path):
    rows = records(read_json(path), "concepts.json")
    result = {}
    for row in rows:
        fields(row, ("key", "value", "claim_id"), "概念登记")
        key = row["key"].strip().casefold()
        require(key not in result, f"概念登记重复 {key}")
        result[key] = row
    return result


def review_files(kind):
    names = (
        "scope_contract.json", "sources.json", "evidence_ledger.json", "evidence_matrix.md",
        "technical_notes.md", "concepts.json", "research.md",
    )
    if kind == "final":
        names += ("review_research.md", "review_research.json", "podcast_source.md", "notebooklm_source_list.md")
    return names


def check_review(path, review_kind, files, run, claim_ids, claims):
    review = read_json(path)
    require(isinstance(review, dict), "审核记录应为对象")
    fields(review, ("episode", "reviewer_id", "review_session", "review_method", "verdict"), review_kind)
    parameters = run["parameters"]
    require(review["episode"] == parameters["episode"] and review["verdict"] == "pass", f"{review_kind} 未通过")
    require(review["reviewer_id"] != parameters["writer_id"] and review["review_session"] != parameters["writer_id"]
            and review["review_method"] in {"independent_agent", "independent_session", "human"},
            "请在独立上下文中完成审核并记录身份")
    if review_kind == "final":
        first = read_json(files["review_research.json"])
        require(review["review_session"] != first["review_session"], "最终审核须使用与母稿审核不同的会话")
    expected = {name: sha256(files[name]) for name in review_files(review_kind)}
    require(review.get("reviewed_sha256") == expected, "审核记录与当前产物快照不一致")
    gates = review.get("hard_gates")
    expected_gates = HARD_GATES | ({"audio_consistency", "package"} if review_kind == "final" else set())
    require(isinstance(gates, dict) and set(gates) == expected_gates and all(v is True for v in gates.values()),
            "独立审核未通过全部硬性门槛")
    scores = review.get("scores")
    require(isinstance(scores, dict) and set(scores) == set(SCORES)
            and all(type(v) is int and 0 <= v <= SCORES[key] for key, v in scores.items()),
            "评分须包含六个维度，分数不能超出权重")
    require(sum(scores.values()) >= PROFILES[parameters["review_profile"]], "总分低于审核档位阈值")
    verified = set(strings(review.get("verified_claims"), "verified_claims", nonempty=True))
    critical = {cid for cid in claim_ids if claims[cid]["critical"]}
    require(critical <= verified <= claim_ids, "审核须覆盖本稿所有核心主张且不得引用未知主张")
    issues = unique(records(review.get("issues"), "审核问题"), "issue_id", r"I\d{2,}")
    for issue in issues.values():
        fields(issue, ("severity", "status", "location", "evidence", "fix", "verification"), "审核问题")
        severity, status = issue["severity"], issue["status"]
        require(severity in {"BLOCKER", "MAJOR", "MINOR"} and status in {"open", "fixed", "accepted"}, "审核问题状态无效")
        require(severity != "BLOCKER" or status == "fixed", "仍存在阻塞项")
        require(severity != "MAJOR" or status in {"fixed", "accepted"}, "仍存在未处理的重大问题")
        if status == "accepted":
            fields(issue, ("rationale",), "接受未修复问题的理由")


def check(stage, files, run):
    for name in STAGES[stage]:
        path = files[name]
        require(path.is_file() and not path.is_symlink() and path.stat().st_size > 0, f"缺少有效产物 {name}")
        if name.endswith(".md"):
            contents = path.read_text(encoding="utf-8")
            require(bool(re.search(r"^#{1,6}\s+\S", contents, re.M)), f"{name} 缺少 Markdown 标题")
            for target in LOCAL_LINK.findall(contents):
                require(target.split("#", 1)[0] in files, f"{name} 引用了不存在的本地文件 {target}")

    episode = run["parameters"]["episode"]
    if stage == "BRIEF_READY":
        contract = read_json(files["scope_contract.json"])
        require(isinstance(contract, dict) and contract.get("episode") == episode, "范围契约期数错误")
        for key in ("include", "preview_only", "exclude", "prerequisites"):
            strings(contract.get(key), key, nonempty=key == "include")
        require(contract["prerequisites"] == run["prerequisites"], "范围契约与课程依赖不一致")
    if stage in ("BRIEF_READY", "PLAN_READY"):
        return

    verified = sources(files["sources.json"], run["parameters"]["as_of_date"])
    if stage == "SOURCES_VERIFIED":
        require(referenced(files["references.md"], SOURCE_REF, verified) == set(verified), "参考文献表未覆盖所有已核验来源")
        return
    claims = evidence(files["evidence_ledger.json"], verified, episode)
    if stage == "EVIDENCE_BUILT":
        require(referenced(files["evidence_matrix.md"], CLAIM_REF, claims) == set(claims), "证据矩阵未覆盖全部主张")
        require(all(row["claim_id"] in claims for row in concepts(files["concepts.json"]).values()), "概念登记引用了未知主张")
        return

    draft = referenced(files["research.md"], CLAIM_REF, claims)
    require({cid for cid, row in claims.items() if row["critical"]} <= draft, "母稿漏掉了账本中的核心主张")
    if stage in {"RESEARCH_REVIEWED", "ACCEPTED"}:
        check_review(files["review_research.json"], "research", files, run, draft, claims)
    if stage in {"PODCAST_DRAFTED", "FINAL_REVIEWED", "ACCEPTED"}:
        audio = referenced(files["podcast_source.md"], CLAIM_REF, draft)
        require(1 <= len(referenced(files["notebooklm_source_list.md"], SOURCE_REF,
                                     {key for key, row in verified.items() if row["kind"] in PRIMARY})) <= 4,
                "NotebookLM 来源清单须列出 1–4 份已核验的一手来源")
        if stage in {"FINAL_REVIEWED", "ACCEPTED"}:
            check_review(files["review_final.json"], "final", files, run, draft | audio, claims)
