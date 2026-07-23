#!/usr/bin/env python3
"""inside-me collector: mine ~/.claude for behavioral stats. Zero deps, local only.

Usage: python3 collect_stats.py [output.json]

Sources, best-first:
  1. ~/.claude/usage-data/session-meta/*.json  (rich; produced by /insights)
  2. ~/.claude/projects/*/*.jsonl              (fallback: light scan of transcripts)
  3. ~/.claude/usage-data/facets/*.json        (optional: LLM per-session analysis)

Nothing leaves the machine. The output may contain prompt fragments — treat it
as private; never commit it.
"""
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone

CLAUDE = os.path.expanduser(os.environ.get("CLAUDE_HOME", "~/.claude"))
OUT = sys.argv[1] if len(sys.argv) > 1 else "stats.json"
PROMPT_CLIP = 180
PROMPTS_PER_PROJECT = 4


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def to_local(iso):
    """ISO timestamp -> local datetime (script runs on the user's machine)."""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.astimezone()
    except (ValueError, AttributeError):
        return None


def project_name(path):
    if not path:
        return "unknown"
    base = os.path.basename(path.rstrip("/"))
    return base or path


def clip(text):
    text = re.sub(r"\s+", " ", (text or "")).strip()
    return text[:PROMPT_CLIP] + ("…" if len(text) > PROMPT_CLIP else "")


# ---------------------------------------------------------------- session-meta
def read_session_meta():
    metadir = os.path.join(CLAUDE, "usage-data", "session-meta")
    if not os.path.isdir(metadir):
        return []
    sessions = []
    for name in os.listdir(metadir):
        if not name.endswith(".json"):
            continue
        m = load_json(os.path.join(metadir, name))
        if m and m.get("start_time"):
            sessions.append(m)
    return sessions


# ---------------------------------------------------- transcripts (fallback)
def read_transcripts_light():
    """Cheap scan: first user prompt + first/last timestamps per session file."""
    projdir = os.path.join(CLAUDE, "projects")
    if not os.path.isdir(projdir):
        return []
    sessions = []
    for d in os.listdir(projdir):
        full = os.path.join(projdir, d)
        if not os.path.isdir(full):
            continue
        for fn in os.listdir(full):
            if not fn.endswith(".jsonl"):
                continue
            path = os.path.join(full, fn)
            first_prompt, first_ts, last_ts = None, None, None
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f):
                        if i > 200 and first_prompt and first_ts:
                            break
                        try:
                            rec = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        ts = rec.get("timestamp")
                        if ts and not first_ts:
                            first_ts = ts
                        if ts:
                            last_ts = ts
                        if not first_prompt and rec.get("type") == "user":
                            msg = rec.get("message") or {}
                            content = msg.get("content")
                            if isinstance(content, str) and content.strip():
                                first_prompt = content
                            elif isinstance(content, list):
                                for part in content:
                                    if isinstance(part, dict) and part.get("type") == "text":
                                        first_prompt = part.get("text")
                                        break
            except OSError:
                continue
            if not first_ts:
                continue
            # reconstruct a decoded project path from the flattened dir name
            sessions.append({
                "session_id": fn[:-6],
                "project_path": d.replace("-", "/"),
                "start_time": first_ts,
                "end_time": last_ts,
                "first_prompt": first_prompt or "",
                "user_message_timestamps": [first_ts],
                "_light": True,
            })
    return sessions


# --------------------------------------------------------------------- facets
def read_facets():
    fdir = os.path.join(CLAUDE, "usage-data", "facets")
    if not os.path.isdir(fdir):
        return []
    out = []
    for name in os.listdir(fdir):
        if name.endswith(".json"):
            f = load_json(os.path.join(fdir, name))
            if f:
                out.append(f)
    return out


# ------------------------------------------------------------------ aggregate
def aggregate(sessions, facets):
    hours, weekdays = Counter(), Counter()
    langs, tools = Counter(), Counter()
    projects = {}
    total = {
        "sessions": len(sessions), "user_messages": 0, "assistant_messages": 0,
        "git_commits": 0, "git_pushes": 0, "lines_added": 0, "lines_removed": 0,
        "files_modified": 0, "input_tokens": 0, "output_tokens": 0,
        "tool_errors": 0, "interruptions": 0,
    }
    durations, response_times, intervals = [], [], []
    first_seen, last_seen = None, None

    for s in sessions:
        start = to_local(s.get("start_time"))
        if start:
            first_seen = min(first_seen, start) if first_seen else start
            last_seen = max(last_seen, start) if last_seen else start
            weekdays[start.weekday()] += 1
            dur = s.get("duration_minutes") or 0
            durations.append(dur)
            if dur:
                intervals.append((start.timestamp(), start.timestamp() + dur * 60))
        for ts in s.get("user_message_timestamps") or []:
            lt = to_local(ts)
            if lt:
                hours[lt.hour] += 1
        for k_src, k_dst in [
            ("user_message_count", "user_messages"),
            ("assistant_message_count", "assistant_messages"),
            ("git_commits", "git_commits"), ("git_pushes", "git_pushes"),
            ("lines_added", "lines_added"), ("lines_removed", "lines_removed"),
            ("files_modified", "files_modified"),
            ("input_tokens", "input_tokens"), ("output_tokens", "output_tokens"),
            ("tool_errors", "tool_errors"), ("user_interruptions", "interruptions"),
        ]:
            total[k_dst] += s.get(k_src) or 0
        for lang, n in (s.get("languages") or {}).items():
            langs[lang] += n
        for tool, n in (s.get("tool_counts") or {}).items():
            tools[tool] += n
        response_times.extend(s.get("user_response_times") or [])

        pname = project_name(s.get("project_path"))
        p = projects.setdefault(pname, {
            "name": pname, "path": s.get("project_path"), "sessions": 0,
            "user_messages": 0, "languages": Counter(), "first_prompts": [],
            "first_seen": None, "last_seen": None,
        })
        p["sessions"] += 1
        p["user_messages"] += s.get("user_message_count") or 0
        for lang, n in (s.get("languages") or {}).items():
            p["languages"][lang] += n
        fp = clip(s.get("first_prompt"))
        if fp and len(p["first_prompts"]) < PROMPTS_PER_PROJECT:
            p["first_prompts"].append(fp)
        if start:
            iso = start.isoformat()
            p["first_seen"] = min(p["first_seen"], iso) if p["first_seen"] else iso
            p["last_seen"] = max(p["last_seen"], iso) if p["last_seen"] else iso

    # multi-clauding: sessions whose [start, end] intervals overlap another's
    intervals.sort()
    overlapping, latest_end = set(), None
    for i, (a, b) in enumerate(intervals):
        if latest_end is not None and a < latest_end[0]:
            overlapping.add(i)
            overlapping.add(latest_end[1])
        if latest_end is None or b > latest_end[0]:
            latest_end = (b, i)

    night = sum(hours[h] for h in range(0, 6))
    all_hours = sum(hours.values()) or 1
    durations.sort()
    response_times.sort()

    def median(xs):
        return xs[len(xs) // 2] if xs else 0

    facet_agg = {
        "outcomes": Counter(), "satisfaction": Counter(),
        "session_types": Counter(), "goal_categories": Counter(),
        "helpfulness": Counter(), "summaries": [],
    }
    for f in facets:
        if f.get("outcome"):
            facet_agg["outcomes"][f["outcome"]] += 1
        if f.get("session_type"):
            facet_agg["session_types"][f["session_type"]] += 1
        if f.get("claude_helpfulness"):
            facet_agg["helpfulness"][f["claude_helpfulness"]] += 1
        for k, v in (f.get("user_satisfaction_counts") or {}).items():
            facet_agg["satisfaction"][k] += v
        for k, v in (f.get("goal_categories") or {}).items():
            facet_agg["goal_categories"][k] += v
        if f.get("brief_summary") and len(facet_agg["summaries"]) < 40:
            facet_agg["summaries"].append(f["brief_summary"])

    for p in projects.values():
        p["languages"] = dict(p["languages"].most_common(5))

    return {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "source": "session-meta" if sessions and not sessions[0].get("_light") else "transcripts-light",
        "span": {
            "first": first_seen.isoformat() if first_seen else None,
            "last": last_seen.isoformat() if last_seen else None,
            "days": (last_seen - first_seen).days + 1 if first_seen and last_seen else 0,
        },
        "totals": total,
        "hour_histogram": {str(h): hours.get(h, 0) for h in range(24)},
        "weekday_histogram": {str(d): weekdays.get(d, 0) for d in range(7)},  # 0=Mon
        "night_pct": round(100 * night / all_hours, 1),
        "peak_hour": max(hours, key=hours.get) if hours else None,
        "languages": dict(langs.most_common(10)),
        "tools": dict(tools.most_common(12)),
        "session_minutes": {
            "median": median(durations),
            "max": durations[-1] if durations else 0,
            "marathons_over_2h": sum(1 for d in durations if d >= 120),
        },
        "response_seconds_median": round(median(response_times), 1),
        "multi_clauding_sessions": len(overlapping),
        "projects": sorted(projects.values(), key=lambda p: -p["sessions"]),
        "facets": {k: (dict(v.most_common()) if isinstance(v, Counter) else v)
                   for k, v in facet_agg.items()},
    }


def main():
    sessions = read_session_meta()
    if not sessions:
        sessions = read_transcripts_light()
    if not sessions:
        sys.exit(f"inside-me: no usable data under {CLAUDE}")
    stats = aggregate(sessions, read_facets())
    os.makedirs(os.path.dirname(os.path.abspath(OUT)) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)
    p = stats["projects"]
    print(f"inside-me: {stats['totals']['sessions']} sessions, "
          f"{len(p)} projects, span {stats['span']['days']}d -> {OUT}")


if __name__ == "__main__":
    main()
