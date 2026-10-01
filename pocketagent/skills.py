"""Agent Skills loader (agentskills.io): SKILL.md with YAML frontmatter, progressive disclosure."""
from dataclasses import dataclass
from pathlib import Path
import re
import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@dataclass
class Skill:
    name: str
    description: str
    path: Path
    body: str = ""

    @property
    def scripts_dir(self) -> Path:
        return self.path / "scripts"


def parse_skill(skill_dir: Path) -> Skill:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{skill_dir}: missing YAML frontmatter")
    meta = yaml.safe_load(m.group(1)) or {}
    name, desc = meta.get("name", ""), meta.get("description", "")
    if not NAME_RE.match(name) or len(name) > 64:
        raise ValueError(f"{skill_dir}: invalid name {name!r}")
    if name != skill_dir.name:
        raise ValueError(f"{skill_dir}: name must match directory")
    if not desc or len(desc) > 1024:
        raise ValueError(f"{skill_dir}: description required, max 1024 chars")
    return Skill(name, desc, skill_dir, m.group(2).strip())


def discover(root: str | Path) -> dict[str, Skill]:
    skills = {}
    for d in sorted(Path(root).iterdir()):
        if (d / "SKILL.md").is_file():
            s = parse_skill(d)
            skills[s.name] = s
    return skills


def catalog(skills: dict[str, Skill]) -> str:
    """Tier 1: only name + description enter the context."""
    return "\n".join(f"- {s.name}: {s.description}" for s in skills.values())
