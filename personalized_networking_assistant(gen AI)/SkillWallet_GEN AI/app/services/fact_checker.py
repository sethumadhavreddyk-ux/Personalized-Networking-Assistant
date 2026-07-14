
import wikipedia


class FactChecker:
    """Validates factual accuracy of generated content via Wikipedia."""

    def __init__(self):
        """Initialize the FactChecker and set language."""
        wikipedia.set_lang("en")

    def check_facts(self, topics: list) -> list:
        """Verify factual accuracy of a list of topic strings."""
        return [self.verify_claim(topic) for topic in topics]

    def verify_claim(self, claim: str) -> dict:
        """Verify a single factual claim against Wikipedia."""
        try:
            search_results = wikipedia.search(claim, results=3)

            if not search_results:
                return {
                    "claim": claim,
                    "verified": False,
                    "confidence": 0.0,
                    "source": "",
                    "summary": "No relevant Wikipedia articles found.",
                }

            try:
                page = wikipedia.page(search_results[0], auto_suggest=False)
                return {
                    "claim": claim,
                    "verified": True,
                    "confidence": 0.85,
                    "source": page.url,
                    "summary": page.summary[:300],
                }

            except wikipedia.DisambiguationError as e:
                try:
                    page = wikipedia.page(e.options[0], auto_suggest=False)
                    return {
                        "claim": claim,
                        "verified": True,
                        "confidence": 0.70,
                        "source": page.url,
                        "summary": page.summary[:300],
                    }
                except Exception:
                    return {
                        "claim": claim,
                        "verified": False,
                        "confidence": 0.30,
                        "source": "",
                        "summary": f"Ambiguous topic. Related: {', '.join(e.options[:5])}",
                    }

            except wikipedia.PageError:
                return {
                    "claim": claim,
                    "verified": False,
                    "confidence": 0.20,
                    "source": "",
                    "summary": "Wikipedia page not found for this topic.",
                }

        except Exception as exc:
            return {
                "claim": claim,
                "verified": False,
                "confidence": 0.0,
                "source": "",
                "summary": f"Verification error: {str(exc)}",
            }