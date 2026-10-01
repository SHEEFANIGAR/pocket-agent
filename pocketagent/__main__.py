import argparse
import sys
from .backends import make_backend


def _add_model_args(p):
    p.add_argument("--model", help="path to a GGUF open-weight model (llama.cpp)")
    p.add_argument("--ollama", metavar="NAME", help="use a local Ollama model instead, e.g. qwen2.5:3b")
    p.add_argument("--host", help="Ollama host (default http://localhost:11434)")
    p.add_argument("--skills", default="skills")


def main():
    ap = argparse.ArgumentParser(prog="pocketagent")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="run a task")
    r.add_argument("task")
    r.add_argument("--no-constrain", action="store_true", help="disable grammar-constrained decoding")
    _add_model_args(r)

    v = sub.add_parser("validate", help="validate skills against the Agent Skills format")
    v.add_argument("path", nargs="?", default="skills")

    b = sub.add_parser("bench", help="constrained vs unconstrained tool-call benchmark")
    b.add_argument("--label", required=True, help="model label for the results table, e.g. qwen2.5-1.5b")
    b.add_argument("--prompts", default="bench/prompts.jsonl")
    _add_model_args(b)

    a = ap.parse_args()
    if a.cmd == "validate":
        from .validate import main as vmain
        sys.exit(vmain(a.path))
    backend = make_backend(a.model, a.ollama, a.host)
    if a.cmd == "run":
        from .agent import Agent
        print(Agent(backend, a.skills, constrained=not a.no_constrain).run(a.task))
    else:
        from .bench import run
        print("| Model | Mode | Strict valid | Lenient valid | Correct skill |")
        print("|---|---|---|---|---|")
        print(run(backend, a.skills, a.prompts, a.label))


if __name__ == "__main__":
    main()
