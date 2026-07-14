
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

from config import get_settings


class EventAnalyzer:

    def __init__(self):
        settings = get_settings()
        self.tokenizer = AutoTokenizer.from_pretrained(settings.DISTILBERT_MODEL)
        self.model = AutoModel.from_pretrained(settings.DISTILBERT_MODEL)
        self.model.eval()
        self.candidate_themes = settings.CANDIDATE_THEMES
        self._theme_embeddings = self._compute_embeddings(self.candidate_themes)

    def _compute_embeddings(self, texts: list) -> torch.Tensor:
        """Compute mean-pooled DistilBERT embeddings for a list of texts."""
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=128,
        )
        with torch.no_grad():
            outputs = self.model(**inputs)

        attention_mask = inputs["attention_mask"]
        token_embeddings = outputs.last_hidden_state
        mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        summed = (token_embeddings * mask_expanded).sum(dim=1)
        counts = mask_expanded.sum(dim=1)
        return summed / counts

    def analyze_event(self, event_name: str, user_role: str) -> dict:
        """Analyze event details and return structured context."""
        themes = self.extract_themes(event_name)
        audience_profile = self._determine_audience(user_role)
        return {
            "event_name": event_name,
            "user_role": user_role,
            "themes": themes,
            "audience_profile": audience_profile,
        }

    def extract_themes(self, event_name: str) -> list:
        """Extract top matching themes using cosine similarity."""
        event_emb = self._compute_embeddings([event_name])
        similarities = F.cosine_similarity(event_emb, self._theme_embeddings)
        top_indices = similarities.argsort(descending=True)[:5]

        themes = []
        for idx in top_indices:
            score = similarities[idx].item()
            if score > 0.3 or not themes:
                themes.append({
                    "theme": self.candidate_themes[idx],
                    "confidence": round(score, 4),
                })
        return themes

    def _determine_audience(self, user_role: str) -> str:
        """Map user role to an audience profile description."""
        role = user_role.lower()

        if any(k in role for k in ["developer", "engineer", "programmer", "architect"]):
            return "Technical professionals focused on implementation and architecture"
        elif any(k in role for k in ["manager", "director", "lead", "vp"]):
            return "Management professionals focused on strategy and team leadership"
        elif any(k in role for k in ["student", "intern", "fresher", "graduate"]):
            return "Early-career individuals seeking learning and mentorship"
        elif any(k in role for k in ["ceo", "founder", "entrepreneur", "cto"]):
            return "Executive leaders focused on vision, growth, and innovation"
        elif any(k in role for k in ["researcher", "scientist", "professor", "academic"]):
            return "Academic professionals focused on research and knowledge advancement"
        elif any(k in role for k in ["designer", "ux", "ui", "creative"]):
            return "Design professionals focused on user experience and creative solutions"
        elif any(k in role for k in ["analyst", "data", "consultant"]):
            return "Analytical professionals focused on insights and data-driven decisions"
        else:
            return f"Professional in {user_role} role seeking networking opportunities"