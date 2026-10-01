#!/bin/sh
# Usage: ./run_bench.sh   (edit the model paths / Ollama tags below)
set -e
echo "| Model | Mode | Strict valid | Lenient valid | Correct skill |"
echo "|---|---|---|---|---|"
python -m pocketagent bench --label qwen2.5-1.5b --model models/qwen2.5-1.5b-instruct-q4_k_m.gguf | tail -n 2
python -m pocketagent bench --label qwen2.5-3b   --model models/qwen2.5-3b-instruct-q4_k_m.gguf   | tail -n 2
# Ollama alternative:
# python -m pocketagent bench --label llama3.2-3b --ollama llama3.2:3b | tail -n 2
