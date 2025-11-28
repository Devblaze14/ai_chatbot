from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


@dataclass
class ChatTurn:
    role: str
    content: str


class LlamaChatModel:
    """
    Beginner‑friendly wrapper around a small LLaMA‑style model.

    The default configuration uses a lightweight chat model so it can run on CPU.
    You can swap the model_name for a larger, fine‑tuned LLaMA model later
    without changing the rest of the application.
    """

    def __init__(
        self,
        model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        device: str | None = None,
        max_new_tokens: int = 128,
    ) -> None:
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_new_tokens = max_new_tokens

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            ).to(self.device)
        except Exception:
            # Fallback: if the model cannot be loaded (e.g. no internet or low RAM),
            # keep a minimal rule‑based engine so the project still runs.
            self.tokenizer = None
            self.model = None

    def _format_history(self, history: List[Dict[str, str]]) -> str:
        parts: List[str] = []
        for turn in history:
            role = turn.get("role", "user").strip().lower()
            content = turn.get("content", "").strip()
            if not content:
                continue
            label = "User" if role == "user" else "Assistant"
            parts.append(f"{label}: {content}")
        return "\n".join(parts)

    def _rule_based_reply(self, message: str, history: List[Dict[str, str]]) -> str:
        text = message.lower()

        if any(word in text for word in ["hello", "hi", "hey"]):
            return "Hi! I’m your 2025 AI chatbot. Ask me anything about our domain and I’ll walk you through it step by step."
        if "help" in text or "how do i" in text:
            return "Tell me what you are trying to do, and I’ll break it down into a clear, beginner‑friendly set of steps."
        if "project" in text:
            return "This chatbot is designed as a small, domain‑aware assistant. It keeps short‑term context so it can respond based on your recent questions."
        if "thanks" in text or "thank you" in text:
            return "You’re welcome! If you have more questions, just send your next message."

        # Use a simple generic fallback to keep answers approachable.
        return (
            "Here’s a concise, beginner‑friendly explanation based on what you asked: "
            "focus on the key idea, understand it with a small example, and then try it yourself. "
            "If you tell me your exact use‑case, I can tailor the answer to your context."
        )

    def generate_reply(self, message: str, history: List[Dict[str, str]]) -> str:
        # If we don't have a real model loaded, fall back to the rule‑based engine.
        if self.model is None or self.tokenizer is None:
            return self._rule_based_reply(message, history)

        conversation = self._format_history(history)
        prompt = (
            "You are a friendly, domain‑specific assistant. "
            "Give short, clear explanations that are easy for beginners in 2025.\n\n"
        )
        if conversation:
            prompt += conversation + "\n"
        prompt += f"User: {message}\nAssistant:"

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the assistant's latest reply.
        if "Assistant:" in full_text:
            reply = full_text.split("Assistant:")[-1].strip()
        else:
            reply = full_text.strip()

        return reply or self._rule_based_reply(message, history)


