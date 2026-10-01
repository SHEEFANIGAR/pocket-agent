"""Model backends. Each exposes chat(messages, schema=None) -> str.
If `schema` is given, output is constrained to that JSON schema."""
import json
import urllib.request


class LlamaCppBackend:
    def __init__(self, model_path: str, n_ctx: int = 4096):
        from llama_cpp import Llama  # lazy: only needed for this backend
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx, verbose=False)

    def chat(self, messages, schema=None) -> str:
        kw = {}
        if schema is not None:
            kw["response_format"] = {"type": "json_object", "schema": schema}
        out = self.llm.create_chat_completion(
            messages=messages, temperature=0.1, max_tokens=512, **kw)
        return out["choices"][0]["message"]["content"]


class OllamaBackend:
    """Talks to a local Ollama server (structured outputs via `format`)."""

    def __init__(self, model: str, host: str = "http://localhost:11434"):
        self.model, self.host = model, host.rstrip("/")

    def chat(self, messages, schema=None) -> str:
        body = {"model": self.model, "messages": messages, "stream": False,
                "options": {"temperature": 0.1, "num_predict": 512}}
        if schema is not None:
            body["format"] = schema
        req = urllib.request.Request(
            f"{self.host}/api/chat", data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)["message"]["content"]


def make_backend(model: str | None = None, ollama: str | None = None, host: str | None = None):
    if ollama:
        return OllamaBackend(ollama, host or "http://localhost:11434")
    if model:
        return LlamaCppBackend(model)
    raise SystemExit("Provide --model PATH.gguf or --ollama NAME")
