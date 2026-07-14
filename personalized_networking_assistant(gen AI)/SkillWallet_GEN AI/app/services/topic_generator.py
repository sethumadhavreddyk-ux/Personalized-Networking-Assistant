
import re
from transformers import pipeline
from config import get_settings
class TopicGenerator:
    def __init__(self):
        settings = get_settings()
        self.generator = pipeline(
            "text-generation",
            model=settings.GPT2_MODEL,
            tokenizer=settings.GPT2_MODEL,
        )
        self.max_new_tokens = settings.MAX_NEW_TOKENS
        self.temperature = settings.TEMPERATURE
        self.top_k = settings.TOP_K
        self.top_p = settings.TOP_P

    def generate_topics(self, event_context: dict, user_interests: list) -> list:
        """Generate a list of conversation topics based on context."""
        themes = [t["theme"] for t in event_context.get("themes", [])]
        combined = list(dict.fromkeys(themes + user_interests))[:5]
        event_name = event_context.get("event_name", "Networking Event")

        topics = []
        for keyword in combined:
            title = f"{keyword} in {event_name}"
            talking_points = self.generate_talking_points(keyword, event_context)
            topics.append({"topic": title, "talking_points": talking_points})

        if not topics:
            topics.append({
                "topic": f"General Networking at {event_name}",
                "talking_points": self._fallback_points("General Networking"),
            })
        return topics

    def generate_talking_points(self, topic: str, event_context: dict = None) -> list:
        """Generate specific talking points for a given topic."""
        prompt = self._build_prompt(topic, event_context)
        try:
            result = self.generator(
                prompt,
                max_new_tokens=self.max_new_tokens,
                num_return_sequences=1,
                temperature=self.temperature,
                top_k=self.top_k,
                top_p=self.top_p,
                do_sample=True,
                pad_token_id=self.generator.tokenizer.eos_token_id,
            )
            generated = result[0]["generated_text"]
            return self._parse_talking_points(generated, prompt, topic)
        except Exception:
            return self._fallback_points(topic)

    def _build_prompt(self, topic: str, event_context: dict = None) -> str:
        event_name = (
            event_context.get("event_name", "a networking event")
            if event_context
            else "a networking event"
        )
        return (
            f"Professional networking conversation about {topic} "
            f"at {event_name}. Key discussion points:\n1."
        )

    def _parse_talking_points(self, text: str, prompt: str, topic: str) -> list:
        new_text = text[len(prompt) - 2:]
        lines = [ln.strip() for ln in new_text.split("\n") if ln.strip()]

        points = []
        for line in lines:
            cleaned = re.sub(r"^\d+[\.\)\-]\s*", "", line).strip()
            if cleaned and len(cleaned) > 10 and len(points) < 3:
                if len(cleaned) > 200:
                    dot = cleaned[:200].rfind(".")
                    cleaned = cleaned[: dot + 1] if dot > 50 else cleaned[:200]
                points.append({"point": cleaned[:80], "details": cleaned})

        return points if points else self._fallback_points(topic)

    def _fallback_points(self, topic: str) -> list:
        return [
            {
                "point": f"Current trends in {topic}",
                "details": f"Discuss the latest developments and emerging trends in {topic}.",
            },
            {
                "point": f"Challenges in {topic}",
                "details": f"Explore common challenges professionals face in {topic} and how to address them.",
            },
            {
                "point": f"Future of {topic}",
                "details": f"Share perspectives on the future direction and upcoming innovations in {topic}.",
            },
        ]