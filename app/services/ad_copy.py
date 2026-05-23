import json
import logging
import re

from app.prompts.ad_copy import ad_copy_prompt
from app.schemas.ad_copy import AdCopyItem, AdCopyRequest
from app.services.doubao import DoubaoService

logger = logging.getLogger(__name__)


class AdCopyService:
    """广告文案生成业务（LangChain 提示词 + 豆包调用）。"""

    def __init__(self, doubao: DoubaoService) -> None:
        self._doubao = doubao

    async def generate(self, request: AdCopyRequest) -> list[AdCopyItem]:
        messages = ad_copy_prompt.format_messages(
            count=request.count,
            prompt=request.prompt,
        )

        logger.info("ad copy generate | prompt_len=%d", len(request.prompt))
        raw = await self._doubao.invoke(messages, model=request.model)
        text = self._doubao.extract_text(raw)
        return self._parse_copies(text)

    @staticmethod
    def _parse_copies(text: str) -> list[AdCopyItem]:
        cleaned = text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("ad copy response is not valid JSON, fallback to plain text")
            return [AdCopyItem(body=cleaned, angle="原始输出")]

        if isinstance(data, dict) and "copies" in data:
            data = data["copies"]
        if not isinstance(data, list):
            return [AdCopyItem(body=cleaned, angle="原始输出")]

        items: list[AdCopyItem] = []
        for row in data:
            if isinstance(row, str):
                items.append(AdCopyItem(body=row))
            elif isinstance(row, dict):
                items.append(
                    AdCopyItem(
                        title=str(row.get("title", "")),
                        body=str(row.get("body", row.get("content", ""))),
                        cta=str(row.get("cta", "")),
                        angle=str(row.get("angle", "")),
                    )
                )
        return items or [AdCopyItem(body=cleaned, angle="原始输出")]
