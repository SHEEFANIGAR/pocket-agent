# PocketAgent

An offline agent harness that lets 1-4B open-weight models (GGUF via llama.cpp, or Ollama)
use [Agent Skills](https://agentskills.io) reliably on CPU-only, no-network devices.

## Why
Small models often break tool calling with malformed or fenced JSON. PocketAgent constrains
every step with a JSON-schema grammar so the action is always valid, and loads skills with
progressive disclosure (catalog -> SKILL.md -> scripts) to fit tiny context windows.

## Quickstart
```bash
pip install -r requirements.txt
# any GGUF works, e.g. Qwen2.5-3B-Instruct-Q4_K_M
python -m pocketagent run "Convert 12 km to miles" --model models/qwen2.5-3b-instruct-q4_k_m.gguf
python -m pocketagent run "Convert 12 km to miles" --ollama qwen2.5:3b      # Ollama backend
python -m pocketagent run "..." --model m.gguf --no-constrain               # baseline decoding
python -m pocketagent validate skills                                       # skill validator
pytest
```

## Bundled skills
| Skill | What it does |
|---|---|
| `csv-summary` | Row count, columns, numeric stats for a CSV |
| `unit-convert` | Length / mass / volume / temperature conversion |
| `note-search` | Keyword search across local .txt/.md notes |
| `pdf-extract` | Text extraction from a PDF (needs `pypdf`) |

Add your own: create `skills/<name>/SKILL.md` (name must match the directory) and run
`python -m pocketagent validate skills`.

## Features
- Grammar-constrained action loop (`activate_skill` / `run_script` / `answer`)
- Backends: llama.cpp (GGUF) and Ollama
- Skill validator CLI (name rules, description length, missing script references)
- Sandboxed script runner: skill-local scripts only, timeout, no shell
- Benchmark harness for constrained vs. unconstrained decoding

## Benchmark
50 prompts (`bench/prompts.jsonl`: 10 each for 4 skills + 10 that need no skill), first-step
action only, same system prompt in both modes, temperature 0.1.

- **Strict valid**: raw output parses as a valid action naming a real skill
- **Lenient valid**: same after stripping ``` fences (a fair baseline)
- **Correct skill**: chose the expected skill, or answered directly when none applies

Reproduce: put GGUFs in `models/`, then `./run_bench.sh`. Results land in `results/*.json`.

| Model | Mode | Strict valid | Lenient valid | Correct skill |
|---|---|---|---|---|
| qwen2.5-1.5b | constrained | _run_bench.sh_ | | |
| qwen2.5-1.5b | unconstrained | | | |
| qwen2.5-3b | constrained | | | |
| qwen2.5-3b | unconstrained | | | |

License: MIT
