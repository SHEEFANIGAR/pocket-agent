import json
from pocketagent.skills import discover
from pocketagent.agent import run_script, Agent, parse_action
from pocketagent.validate import validate_dir
from pocketagent.bench import run


class Scripted:
    def __init__(self, outs):
        self.outs = list(outs)

    def chat(self, messages, schema=None):
        return self.outs.pop(0)


def test_discover_and_csv(tmp_path):
    skills = discover("skills")
    assert {"csv-summary", "unit-convert", "note-search", "pdf-extract"} <= set(skills)
    f = tmp_path / "d.csv"
    f.write_text("a,b\n1,2\n3,4\n")
    assert "rows: 2" in run_script(skills["csv-summary"], "summarize.py", [str(f)])


def test_path_escape_blocked():
    assert run_script(discover("skills")["csv-summary"], "../SKILL.md", []).startswith("ERROR")


def test_unit_convert():
    s = discover("skills")["unit-convert"]
    assert "7.4565 mi" in run_script(s, "convert.py", ["12", "km", "mi"])
    assert "37.0000 c" in run_script(s, "convert.py", ["98.6", "f", "c"])
    assert "ERROR" in run_script(s, "convert.py", ["1", "kg", "km"])


def test_note_search(tmp_path):
    (tmp_path / "a.md").write_text("buy milk\nVaccine fridge temp check\n")
    s = discover("skills")["note-search"]
    out = run_script(s, "search.py", [str(tmp_path), "vaccine fridge"])
    assert "a.md:2" in out
    assert run_script(s, "search.py", [str(tmp_path), "zzz"]).strip() == "no matches"


def test_pdf_extract_errors_gracefully():
    out = run_script(discover("skills")["pdf-extract"], "extract.py", ["/nonexistent.pdf"])
    assert "ERROR" in out


def test_agent_loop_with_fake_backend():
    acts = [{"action": "activate_skill", "skill": "unit-convert"},
            {"action": "run_script", "skill": "unit-convert", "script": "convert.py", "args": ["10", "km", "mi"]},
            {"action": "answer", "text": "10 km = 6.2137 mi"}]
    assert Agent(Scripted(map(json.dumps, acts)), "skills").run("10 km in miles", verbose=False).endswith("6.2137 mi")


def test_agent_recovers_from_bad_json():
    out = Agent(Scripted(["not json", json.dumps({"action": "answer", "text": "ok"})]),
                "skills").run("hi", verbose=False)
    assert out == "ok"


def test_parse_action_lenient_fences():
    raw = '```json\n{"action": "answer", "text": "x"}\n```'
    assert parse_action(raw, lenient=True)["text"] == "x"
    try:
        parse_action(raw)
        assert False
    except ValueError:
        pass
    except json.JSONDecodeError:
        pass


def test_validator_passes_bundled_skills():
    res = validate_dir("skills")
    assert len(res) == 4
    assert all(not [i for i in v if i[0] == "ERROR"] for v in res.values())


def test_validator_catches_errors(tmp_path):
    d = tmp_path / "Bad_Name"
    d.mkdir()
    (d / "SKILL.md").write_text("---\nname: Bad_Name\ndescription: x\n---\nRun scripts/missing.py\n")
    errs = [m for lvl, m in validate_dir(tmp_path)["Bad_Name"] if lvl == "ERROR"]
    assert len(errs) >= 2


def test_bench_math(tmp_path):
    class Oracle:  # always activates unit-convert
        def chat(self, messages, schema=None):
            return '```json\n{"action":"activate_skill","skill":"unit-convert"}\n```'
    row = run(Oracle(), "skills", "bench/prompts.jsonl", "oracle", out_dir=str(tmp_path))
    lines = row.splitlines()
    assert "| constrained | 0% | 100% | 20% |" in lines[0]  # fenced -> strict fail, lenient ok, 10/50 correct
