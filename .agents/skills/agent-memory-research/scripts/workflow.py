"""CLI for repeatable, checkpointed episode production."""

import argparse
import contextlib
import hashlib
import json
import os
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

import fcntl

import gates
from outline import WorkflowError, ordered, parse_outline, scope, select, sha256


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
STATES = ("UNPLANNED", *gates.STAGES)
START_MODES = ("plan", "research", "batch")
PAUSES = {"tool": "BLOCKED", "source": "BLOCKED", "quality": "NEEDS_REVISION"}


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def fingerprint(data):
    return hashlib.sha256(canonical(data)).hexdigest()


def skill_hash():
    files = [ROOT / "SKILL.md"]
    for directory in ("scripts", "references", "assets", "agents"):
        files.extend(path for path in (ROOT / directory).rglob("*")
                     if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc")
    return fingerprint({str(p.relative_to(ROOT)): sha256(p) for p in files})


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        temp = Path(stream.name)
        try:
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
            os.replace(temp, path)
        finally:
            temp.unlink(missing_ok=True)


@contextlib.contextmanager
def locked(run_dir):
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / ".lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def read_run(run_dir):
    return gates.read_json(run_dir / "manifest.json")


def event(run, action, reason="", details=None):
    run["events"].append({
        "time": now(), "action": action, "state": run["state"], "checkpoint": run["checkpoint"],
        "reason": reason, "details": details or {},
    })


def run_path(output, episode, parameters):
    return output / "runs" / episode / fingerprint(parameters)[:24]


def active_files(run_dir, run):
    files = {}
    for name, item in run["artifacts"].items():
        candidate = run_dir / item["path"]
        gates.require(candidate.resolve().is_relative_to(run_dir / "checkpoints")
                      and candidate.is_file() and not candidate.is_symlink()
                      and sha256(candidate) == item["sha256"], f"检查点产物丢失或变更 {name}")
        files[name] = candidate
    expected = {name for stage in STATES[1:STATES.index(run["checkpoint"]) + 1] for name in gates.STAGES[stage]}
    gates.require(set(files) == expected, "检查点产物清单不完整")
    return files


def assert_inputs(run_dir, run):
    parameters = run["parameters"]
    gates.require(sha256(parameters["outline_path"]) == parameters["outline_sha256"], "大纲已变更，请启动新运行")
    gates.require(skill_hash() == parameters["skill_sha256"], "Skill 已变更，请启动新运行")
    gates.require(sha256(run_dir / "scope_input.json") == run["scope_sha256"], "初始范围快照损坏")


def next_stage(run):
    if run["state"] != run["checkpoint"] or run["checkpoint"] == "ACCEPTED":
        return None
    return STATES[STATES.index(run["checkpoint"]) + 1]


def inbox(run_dir, run):
    return run_dir / "work" / f"{len(run['events']):03}"


def describe(run_dir, run):
    stage = next_stage(run)
    work = inbox(run_dir, run) if stage else None
    if work:
        work.mkdir(parents=True, exist_ok=True)
    summary = {
        "run_dir": str(run_dir), "run_id": run_dir.name,
        "episode": run["parameters"]["episode"], "parameters": run["parameters"],
        "state": run["state"], "checkpoint": run["checkpoint"],
        "next_stage": stage, "work_dir": str(work) if work else None,
        "attempt": len(run["events"]), "expected_files": list(gates.STAGES[stage]) if stage else [],
        "scope_input": str(run_dir / "scope_input.json"),
        "artifacts": {name: {**record, "path": str(run_dir / record["path"])}
                      for name, record in run["artifacts"].items()},
        "revisions": run["revisions"], "last_event": run["events"][-1],
        "last_failed_check": (run.get("failed_checks") or [None])[-1],
    }
    if stage in {"RESEARCH_REVIEWED", "FINAL_REVIEWED"}:
        names = gates.review_files("research" if stage == "RESEARCH_REVIEWED" else "final")
        summary["reviewed_sha256"] = {name: run["artifacts"][name]["sha256"] for name in names}
    return summary


def write_index(index, output):
    path = output / "course" / index["outline_sha256"] / "course_index.json"
    write_json(path, index)
    return path


def accepted_runs(output, outline_sha, as_of):
    accepted = {}
    for path in sorted((output / "runs").glob("EP*/[0-9a-f]*/manifest.json")):
        run = read_run(path.parent)
        parameters = run["parameters"]
        if (run["state"] == "ACCEPTED" and parameters["outline_sha256"] == outline_sha
                and parameters["as_of_date"] == as_of):
            files = active_files(path.parent, run)
            gates.check("ACCEPTED", files, run)
            episode = parameters["episode"]
            finished = run["events"][-1]["time"]
            if episode not in accepted or finished > accepted[episode]["accepted_at"]:
                accepted[episode] = {"run_dir": str(path.parent), "accepted_at": finished,
                                     "concepts": gates.concepts(files["concepts.json"])}
    return accepted


def course_index(args):
    return parse_outline(args.outline, expected_episodes=args.expected_episodes, expected_topics=args.expected_topics)


def index_command(args):
    index = course_index(args)
    if args.output_dir:
        write_index(index, args.output_dir.resolve())
    return index


def batch_command(args):
    index = course_index(args)
    output = args.output_dir.resolve()
    path = write_index(index, output)
    selected = select(index, args.episode)
    queue = ordered(index, selected)
    accepted = accepted_runs(output, index["outline_sha256"], args.as_of_date)
    return {
        "index": str(path), "requested": selected, "queue": [
            {"episode": key, "state": "ACCEPTED" if key in accepted else "PENDING",
             "prerequisites": index["episodes"][key]["prerequisites"]}
            for key in queue
        ],
        "accepted": {key: item["run_dir"] for key, item in accepted.items()},
    }


def copy_checkpoint(run_dir, stage, source_files):
    root = run_dir / "checkpoints"
    root.mkdir(exist_ok=True)
    destination = root / uuid.uuid4().hex
    with tempfile.TemporaryDirectory(dir=root) as directory:
        temporary = Path(directory) / "stage"
        temporary.mkdir()
        for name, path in source_files.items():
            gates.require(path.is_file() and not path.is_symlink(), f"缺少有效产物 {name}")
            shutil.copyfile(path, temporary / name)
        temporary.rename(destination)
    return {
        name: {"stage": stage, "path": str((destination / name).relative_to(run_dir)),
               "sha256": sha256(destination / name)}
        for name in source_files
    }


def seed_plan(run_dir, run, unrefreshed, base):
    if not (unrefreshed / "manifest.json").exists():
        return
    with locked(unrefreshed):
        old = read_run(unrefreshed)
        if old["parameters"] != base or STATES.index(old["checkpoint"]) < STATES.index("PLAN_READY"):
            return
        files = active_files(unrefreshed, old)
        for stage in ("BRIEF_READY", "PLAN_READY"):
            run["artifacts"].update(copy_checkpoint(run_dir, stage, {name: files[name] for name in gates.STAGES[stage]}))
            run["state"] = run["checkpoint"] = stage
            event(run, "reuse", "刷新来源，保留计划", {"from_run": unrefreshed.name, "artifacts": gates.STAGES[stage]})


def start_command(args):
    index = course_index(args)
    [episode] = select_single(index, args.episode)
    output = args.output_dir.resolve()
    gates.require(0 <= args.max_revisions <= 20, "max_revisions 须为 0 至 20")
    gates.require(bool(args.writer_id.strip()), "writer_id 不能为空")
    gates.require(args.force_refresh_sources == bool(args.refresh_id), "刷新来源时须提供 --force-refresh-sources 和 --refresh-id")
    base = {
        "outline_path": index["outline"], "outline_sha256": index["outline_sha256"], "episode": episode,
        "as_of_date": args.as_of_date, "depth": args.depth, "output_dir": str(output),
        "max_revisions": args.max_revisions, "review_profile": args.review_profile,
        "writer_id": args.writer_id, "skill_version": VERSION, "skill_sha256": skill_hash(),
        "execution_policy": "batch" if args.mode == "batch" else "single",
        "force_refresh_sources": False, "refresh_id": None,
    }
    parameters = {**base, "force_refresh_sources": args.force_refresh_sources, "refresh_id": args.refresh_id}
    run_dir = run_path(output, episode, parameters)
    with locked(run_dir):
        if (run_dir / "manifest.json").exists():
            run = read_run(run_dir)
            gates.require(run["parameters"] == parameters, "运行 ID 碰撞")
            assert_inputs(run_dir, run)
            active_files(run_dir, run)
            if args.mode == "batch":
                enforce_batch(output, run)
            return describe(run_dir, run)
        bounds = scope(index, episode)
        scope_path = run_dir / "scope_input.json"
        write_json(scope_path, bounds)
        write_index(index, output)
        run = {
            "schema": 1, "created_at": now(), "mode": args.mode, "parameters": parameters,
            "scope_sha256": sha256(scope_path), "prerequisites": index["episodes"][episode]["prerequisites"],
            "state": "UNPLANNED", "checkpoint": "UNPLANNED", "revisions": 0, "artifacts": {}, "events": [],
        }
        if args.mode == "batch":
            enforce_batch(output, run)
        event(run, "start")
        if args.force_refresh_sources:
            seed_plan(run_dir, run, run_path(output, episode, base), base)
        write_json(run_dir / "manifest.json", run)
        return describe(run_dir, run)


def enforce_batch(output, run):
    parameters = run["parameters"]
    accepted = accepted_runs(output, parameters["outline_sha256"], parameters["as_of_date"])
    missing = set(run["prerequisites"]) - set(accepted)
    gates.require(not missing, f"批量运行须先验收前置期 {', '.join(sorted(missing))}")


def select_single(index, expression):
    selection = select(index, expression)
    gates.require(len(selection) == 1, "start 一次处理一期，范围或主题请使用 batch")
    return selection


def conflicts(run, files):
    current = gates.concepts(files["concepts.json"])
    parameters = run["parameters"]
    others = accepted_runs(Path(parameters["output_dir"]), parameters["outline_sha256"], parameters["as_of_date"])
    findings = []
    for episode, record in others.items():
        if episode == parameters["episode"]:
            continue
        for key in sorted(current.keys() & record["concepts"].keys()):
            previous, candidate = record["concepts"][key], current[key]
            if previous["value"].strip().casefold() != candidate["value"].strip().casefold():
                findings.append({"key": key, "prior_episode": episode, "prior": previous, "current": candidate,
                                 "current_episode": parameters["episode"], "prior_run": record["run_dir"]})
    return findings


def advance(args, run_dir, run, files):
    stage = next_stage(run)
    gates.require(stage == args.stage and args.attempt == len(run["events"]), "状态或尝试编号已变更，请重新读取 status")
    if run["mode"] == "batch":
        enforce_batch(Path(run["parameters"]["output_dir"]), run)
    source_files = {name: inbox(run_dir, run) / name for name in gates.STAGES[stage]}
    copied = {}
    try:
        records = copy_checkpoint(run_dir, stage, source_files)
        copied = {name: run_dir / item["path"] for name, item in records.items()}
        combined = {**files, **copied}
        gates.check(stage, combined, run)
        details = {"artifacts": records}
        if stage == "EVIDENCE_BUILT":
            details["cross_episode_conflicts"] = conflicts(run, combined)
    except (ValueError, OSError) as error:
        if copied:
            shutil.rmtree(next(iter(copied.values())).parent)
        run.setdefault("failed_checks", []).append({
            "time": now(), "stage": stage, "attempt": args.attempt, "reason": str(error),
        })
        write_json(run_dir / "manifest.json", run)
        raise
    run["artifacts"].update(records)
    run["state"] = run["checkpoint"] = stage
    event(run, "advance", details=details)


def rewind(args, run):
    gates.require(STATES.index(args.to) < STATES.index(run["checkpoint"]), "修订必须回退到更早的有效检查点")
    gates.require(run["revisions"] < run["parameters"]["max_revisions"], "已到达修订上限，请保留阻塞记录")
    run["revisions"] += 1
    invalidated = {name: item for name, item in run["artifacts"].items() if STATES.index(item["stage"]) > STATES.index(args.to)}
    run["artifacts"] = {name: item for name, item in run["artifacts"].items() if name not in invalidated}
    run["state"] = run["checkpoint"] = args.to
    event(run, "rewind", args.reason, {"invalidated": invalidated})


def release(run_dir, run, files):
    gates.require(run["state"] == "ACCEPTED", "只能导出已验收的资料包")
    gates.check("ACCEPTED", files, run)
    version = fingerprint({name: sha256(path) for name, path in files.items()})[:16]
    destination = run_dir / "releases" / version
    destination.parent.mkdir(exist_ok=True)
    if destination.exists():
        package = gates.read_json(destination / "manifest.json")
        gates.require(package["version"] == version and set(package["artifacts"]) == set(files)
                      and all(sha256(destination / name) == record["sha256"] == sha256(files[name])
                              for name, record in package["artifacts"].items()), "已有导出包损坏")
    else:
        with tempfile.TemporaryDirectory(dir=destination.parent) as directory:
            temporary = Path(directory) / "package"
            temporary.mkdir()
            for name, path in files.items():
                shutil.copyfile(path, temporary / name)
            manifest = {
                "version": version, "run_id": run_dir.name, "state": "ACCEPTED",
                "parameters": run["parameters"], "accepted_at": run["events"][-1]["time"],
                "source_count": len(gates.sources(files["sources.json"], run["parameters"]["as_of_date"])),
                "claim_count": len(gates.read_json(files["evidence_ledger.json"])),
                "audits": [gates.read_json(files[name]) for name in ("review_research.json", "review_final.json")],
                "artifacts": {name: {"path": name, "sha256": sha256(path)} for name, path in files.items()},
            }
            write_json(temporary / "manifest.json", manifest)
            temporary.rename(destination)
    return {"release_dir": str(destination), "version": version, "notebooklm_input": "podcast_source.md"}


def existing_command(args):
    run_dir = args.run.resolve()
    gates.require((run_dir / "manifest.json").is_file(), f"找不到运行清单 {run_dir}")
    with locked(run_dir):
        run = read_run(run_dir)
        files = active_files(run_dir, run)
        command = args.command
        if hasattr(args, "reason"):
            gates.require(bool(args.reason.strip()), "请填写原因")
        if command == "status":
            return describe(run_dir, run)
        if command == "release":
            return release(run_dir, run, files)
        assert_inputs(run_dir, run)
        if command == "conflicts":
            gates.require("concepts.json" in files, "请先建立证据账本和概念登记")
            return {"conflicts": conflicts(run, files)}
        if command == "advance":
            advance(args, run_dir, run, files)
        elif command == "pause":
            gates.require(next_stage(run) is not None, "仅能暂停正在进行的运行")
            run["state"] = PAUSES[args.kind]
            event(run, "pause", args.reason, {"kind": args.kind, "remedy": args.remedy, "paused_inbox": f"{len(run['events']):03}"})
        elif command == "resume":
            gates.require(run["state"] in PAUSES.values(), "运行未暂停，可直接使用 status")
            if run["state"] == "NEEDS_REVISION":
                gates.require(run["revisions"] < run["parameters"]["max_revisions"], "已到达修订上限")
                run["revisions"] += 1
            pause = run["events"][-1]["details"]
            run["state"] = run["checkpoint"]
            event(run, "resume", args.reason, {"prior_inbox": pause["paused_inbox"]})
        elif command == "rewind":
            rewind(args, run)
        write_json(run_dir / "manifest.json", run)
        return describe(run_dir, run)


def input_path(parser):
    parser.add_argument("--outline", type=Path, default=Path("reference/01_Agent_Memory_内容主线.md"))
    parser.add_argument("--expected-episodes", type=int)
    parser.add_argument("--expected-topics", type=int)


def run_parameters(parser):
    input_path(parser)
    parser.add_argument("--episode", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/agent-memory"))
    parser.add_argument("--as-of-date", default=datetime.now().astimezone().date().isoformat())


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    index = commands.add_parser("index")
    input_path(index)
    index.add_argument("--output-dir", type=Path)
    batch = commands.add_parser("batch")
    run_parameters(batch)
    start = commands.add_parser("start")
    run_parameters(start)
    start.add_argument("--mode", choices=START_MODES, default="research")
    start.add_argument("--depth", choices=("deep", "focused"), default="deep")
    start.add_argument("--writer-id", default="codex-writer")
    start.add_argument("--review-profile", choices=gates.PROFILES, default="standard-v1")
    start.add_argument("--max-revisions", type=int, default=2)
    start.add_argument("--force-refresh-sources", action="store_true")
    start.add_argument("--refresh-id")
    for name in ("status", "advance", "pause", "resume", "rewind", "release", "conflicts"):
        command = commands.add_parser(name)
        command.add_argument("--run", type=Path, required=True)
        if name == "advance":
            command.add_argument("--stage", choices=gates.STAGES, required=True)
            command.add_argument("--attempt", type=int, required=True)
        if name in {"pause", "resume", "rewind"}:
            command.add_argument("--reason", required=True)
        if name == "pause":
            command.add_argument("--kind", choices=PAUSES, required=True)
            command.add_argument("--remedy", required=True)
        if name == "rewind":
            command.add_argument("--to", choices=STATES[:-1], required=True)
    return parser.parse_args()


def main():
    args = cli()
    handlers = {"index": index_command, "batch": batch_command, "start": start_command}
    try:
        if hasattr(args, "as_of_date"):
            gates.iso_date(args.as_of_date, "as_of_date")
        if args.command in handlers:
            result = handlers[args.command](args)
        else:
            result = existing_command(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        print(json.dumps({"error": str(error), "command": args.command}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
