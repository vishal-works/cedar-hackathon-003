"""Agent 2: Response Formatter - Converts analysis to structured JSON."""

import json
from openai import OpenAI
from pydantic import ValidationError
from .config import FORMATTER_AGENT, get_openai_api_key
from .schemas import ZoningResponse


class ResponseFormatter:
    """Agent that formats analysis into structured JSON."""

    def __init__(self):
        self.client = OpenAI(api_key=get_openai_api_key())
        self.config = FORMATTER_AGENT

    def format(self, original_query: str, analysis: str) -> ZoningResponse:
        """Format analysis into structured response."""

        user_message = f"""## Original User Query
{original_query}

## Zoning Analysis to Format
{analysis}

Convert the above analysis into the required JSON schema. Output ONLY valid JSON."""

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": self.config.system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            response_format={"type": "json_object"},  # Force JSON output
        )

        raw_json = response.choices[0].message.content

        try:
            data = json.loads(raw_json)
            return ZoningResponse.model_validate(data)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Failed to parse JSON: {exc}\nRaw output: {raw_json}") from exc
        except ValidationError as exc:
            raise ValueError(f"Response validation failed: {exc}\nRaw output: {raw_json}") from exc

    def format_raw(self, original_query: str, analysis: str) -> dict:
        """Format analysis and return raw dict (skip validation)."""

        user_message = f"""## Original User Query
{original_query}

## Zoning Analysis to Format
{analysis}

Convert the above analysis into the required JSON schema. Output ONLY valid JSON."""

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": self.config.system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

