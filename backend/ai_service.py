import os
import json
import httpx

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-opus-4-6"

SYSTEM_PROMPT = """You are a compassionate and insightful journaling assistant.
Your role is to help users reflect on their daily experiences with empathy and depth.
When given a journal entry, analyse it and return ONLY a valid JSON object — no extra text, no markdown fences.

The JSON must follow this exact structure:
{
  "mood": {
    "label": "<one or two word mood, e.g. Reflective, Anxious, Grateful, Content>",
    "score": <integer 1-10, where 1=very negative, 10=very positive>,
    "color": "<one of: teal, blue, amber, coral, purple>"
  },
  "summary": "<2-3 sentence warm and empathetic summary of the entry>",
  "actions": [
    "<actionable reflection or suggestion 1>",
    "<actionable reflection or suggestion 2>",
    "<actionable reflection or suggestion 3>"
  ],
  "themes": ["<theme 1>", "<theme 2>", "<theme 3>"]
}

Guidelines:
- mood.score should honestly reflect the emotional tone (not artificially positive)
- mood.color: teal=calm/peaceful, blue=sad/melancholy, amber=anxious/stressed, coral=angry/frustrated, purple=thoughtful/reflective
- summary should feel human and warm, not clinical
- actions should be specific and actionable, not generic platitudes
- themes are 1-3 word topic tags extracted from the entry
"""


async def generate_insights(entry_content: str) -> dict:
    """Call the Claude API and return a structured insights dict."""
    if not ANTHROPIC_API_KEY:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Please set it before running the server."
        )

    payload = {
        "model": MODEL,
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": f"Please analyse this journal entry:\n\n{entry_content}",
            }
        ],
    }

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(ANTHROPIC_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(
            f"Anthropic API error {response.status_code}: {response.text}"
        )

    data = response.json()
    raw_text = data["content"][0]["text"].strip()

    # Strip markdown fences if the model adds them despite instructions
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    return json.loads(raw_text)
