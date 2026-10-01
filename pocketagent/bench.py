"""First-step tool-call benchmark: constrained vs unconstrained decoding.

Metrics per mode (same prompts, same system prompt):
  strict  - raw output is valid JSON with a known action and skill
  lenient - same, after stripping ``` code fences
  correct - chose the expected skill (or answered directly for no-skill prompts)
"""
import json
from pathlib import Path
from .agent import ACTION_SCHEMA, parse_action, system_prompt
from .skills import discover


def _try(raw, skills, lenient):
    try:
        act = parse_action(raw, lenient=lenient)
    except (ValueError, json.JSONDecodeError):
        return None
    if act["action"] == "answer":
        return act if isinstance(act.get("text"), str) else None
    return act if act.get("skill") in skills else None


def _correct(act, expected) -> bool:
    if expected is None:
        return act["action"] == "answer"
    return act["action"] in ("activate_skill", "run_script") and act["skill"] == expected


def evaluate(backend, skills, prompts, constrained: bool) -> dict:
    sysmsg = system_prompt(skills)
    r = {"n": 0, "strict": 0, "lenient": 0, "correct": 0}
    for p in prompts:
        raw = backend.chat([{"role": "system", "content": sysmsg},
                            {"role": "user", "content": p["prompt"]}],
                           ACTION_SCHEMA if constrained else None)
        strict, lenient = _try(raw, skills, False), _try(raw, skills, True)
        r["n"] += 1
        r["strict"] += strict is not None
        r["lenient"] += lenient is not None
        r["correct"] += lenient is not None and _correct(lenient, p["expected"])
    return r


def load_prompts(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def run(backend, skills_dir, prompts_path, label, out_dir="results") -> str:
    skills, prompts = discover(skills_dir), load_prompts(prompts_path)
    res = {m: evaluate(backend, skills, prompts, m == "constrained")
           for m in ("constrained", "unconstrained")}
    Path(out_dir).mkdir(exist_ok=True)
    Path(out_dir, f"{label}.json").write_text(json.dumps(res, indent=2))
    pct = lambda k, v: f"{100 * v[k] / v['n']:.0f}%"
    return "\n".join(
        f"| {label} | {m} | {pct('strict', v)} | {pct('lenient', v)} | {pct('correct', v)} |"
        for m, v in res.items())
