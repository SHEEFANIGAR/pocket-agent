"""`pocketagent validate DIR` - check skills against the Agent Skills format."""
import re
from pathlib import Path
import yaml

ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill(d: Path) -> list[tuple[str, str]]:
    issues = []
    err = lambda m: issues.append(("ERROR", m))
    warn = lambda m: issues.append(("WARN", m))
    text = (d / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return [("ERROR", "missing YAML frontmatter")]
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return [("ERROR", f"invalid YAML: {e}")]
    body = m.group(2).strip()
    name, desc = meta.get("name"), meta.get("description")
    if not isinstance(name, str) or not name:
        err("missing 'name'")
    else:
        if len(name) > 64 or not NAME_RE.match(name):
            err("name must be lowercase letters/digits/hyphens, <=64 chars, no leading/trailing/double hyphen")
        if name != d.name:
            err(f"name '{name}' must match directory '{d.name}'")
    if not isinstance(desc, str) or not desc.strip():
        err("missing 'description'")
    elif len(desc) > 1024:
        err("description exceeds 1024 chars")
    elif "use when" not in desc.lower():
        warn("description should say when to use the skill ('Use when ...')")
    if isinstance(meta.get("compatibility"), str) and len(meta["compatibility"]) > 500:
        err("compatibility exceeds 500 chars")
    for k in set(meta) - ALLOWED:
        warn(f"unknown frontmatter field '{k}'")
    if not body:
        warn("empty instructions body")
    if len(body.splitlines()) > 500:
        warn("body over 500 lines; move detail into references/")
    for ref in sorted(set(re.findall(r"scripts/[\w./-]*\w", body))):
        if not (d / ref).is_file():
            err(f"referenced file not found: {ref}")
    return issues


def validate_dir(root) -> dict[str, list[tuple[str, str]]]:
    root = Path(root)
    dirs = [root] if (root / "SKILL.md").is_file() else sorted(
        p for p in root.iterdir() if (p / "SKILL.md").is_file())
    return {d.name: validate_skill(d) for d in dirs}


def main(root) -> int:
    results = validate_dir(root)
    if not results:
        print(f"No skills found in {root}")
        return 1
    bad = 0
    for name, issues in results.items():
        errs = [i for i in issues if i[0] == "ERROR"]
        bad += bool(errs)
        print(f"{'FAIL' if errs else 'ok  '} {name}")
        for lvl, msg in issues:
            print(f"     {lvl}: {msg}")
    print(f"\n{len(results) - bad}/{len(results)} skills valid")
    return 1 if bad else 0
