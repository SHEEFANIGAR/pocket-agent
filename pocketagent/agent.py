"""Minimal harness: grammar-constrained action loop for small local models."""
import json
import re
import subprocess
import sys
from .skills import discover, catalog, Skill

ACTIONS = ["activate_skill", "run_script", "answer"]
ACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"enum": ACTIONS},
        "skill": {"type": "string"},
        "script": {"type": "string"},
        "args": {"type": "array", "items": {"type": "string"}},
        "text": {"type": "string"},
    },
    "required": ["action"],
}

SYSTEM = """You are an offline assistant. Respond ONLY with a JSON action.
Actions: activate_skill(skill) to read a skill's instructions; run_script(skill, script, args) to run one of its scripts; answer(text) to finish.
Use a skill when the task matches its description; otherwise answer directly.
Available skills:
{catalog}"""


def system_prompt(skills) -> str:
    return SYSTEM.format(catalog=catalog(skills))


def parse_action(raw: str, lenient: bool = False) -> dict:
    s = raw.strip()
    if lenient:  # tolerate ```json fences (used for unconstrained baselines)
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    act = json.loads(s)
    if not isinstance(act, dict) or act.get("action") not in ACTIONS:
        raise ValueError("invalid action")
    return act


def run_script(skill: Skill, script: str, args: list[str], timeout: int = 20) -> str:
    target = (skill.scripts_dir / script).resolve()
    if skill.scripts_dir.resolve() not in target.parents or not target.is_file():
        return "ERROR: script not found in skill's scripts/ directory"
    try:
        r = subprocess.run([sys.executable, str(target), *map(str, args)],
                           capture_output=True, text=True, timeout=timeout)
        return (r.stdout + r.stderr)[:4000]
    except subprocess.TimeoutExpired:
        return "ERROR: timeout"


class Agent:
    def __init__(self, backend, skills_dir: str, max_steps: int = 6, constrained: bool = True):
        self.backend = backend
        self.skills = discover(skills_dir)
        self.max_steps = max_steps
        self.constrained = constrained

    def run(self, task: str, verbose: bool = True) -> str:
        msgs = [{"role": "system", "content": system_prompt(self.skills)},
                {"role": "user", "content": task}]
        for _ in range(self.max_steps):
            raw = self.backend.chat(msgs, ACTION_SCHEMA if self.constrained else None)
            msgs.append({"role": "assistant", "content": raw})
            try:
                act = parse_action(raw, lenient=not self.constrained)
            except (ValueError, json.JSONDecodeError):
                msgs.append({"role": "user", "content": "OBSERVATION:\nERROR: invalid JSON action"})
                continue
            if verbose:
                print("->", act, file=sys.stderr)
            if act["action"] == "answer":
                return act.get("text", "")
            skill = self.skills.get(act.get("skill", ""))
            if skill is None:
                obs = "ERROR: unknown skill"
            elif act["action"] == "activate_skill":
                obs = skill.body  # Tier 2: full instructions on demand
            else:
                obs = run_script(skill, act.get("script", ""), act.get("args", []))
            msgs.append({"role": "user", "content": f"OBSERVATION:\n{obs}"})
        return "Stopped: step limit reached."
