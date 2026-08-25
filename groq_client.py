import logging
import os

import streamlit as st
from groq import Groq
import groq as _groq

logger = logging.getLogger(__name__)

# Ordered by preference; if the first model has been deprecated/removed on
# Groq's side (404), the next one is tried automatically instead of failing.
TEXT_MODELS = ["openai/gpt-oss-120b", "qwen/qwen3.6-27b"]
VISION_MODELS = ["qwen/qwen3.6-27b"]

MAX_HISTORY_MESSAGES = 20


class GroqAPIError(Exception):
    pass


def _get_client() -> Groq:
    api_key = st.secrets.get("GROQ_API_KEY", "") or os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise GroqAPIError("missing_key")
    return Groq(api_key=api_key)


def _handle_groq_error(exc: Exception) -> GroqAPIError:
    if isinstance(exc, _groq.RateLimitError):
        logger.warning("Groq rate limit hit: %s", exc)
        return GroqAPIError("rate_limit")
    if isinstance(exc, _groq.APIConnectionError):
        logger.error("Groq connection error: %s", exc)
        return GroqAPIError("connection")
    if isinstance(exc, _groq.AuthenticationError):
        logger.error("Groq auth error: %s", exc)
        return GroqAPIError("invalid_key")
    if isinstance(exc, _groq.APIStatusError):
        logger.error("Groq API status %s: %s", exc.status_code, exc.message)
        return GroqAPIError("api_error")
    logger.exception("Unexpected Groq error: %s", exc)
    return GroqAPIError("generic")


def _create_with_fallback(models: list[str], **kwargs) -> str:
    client = _get_client()
    last_exc: Exception | None = None
    for model in models:
        try:
            response = client.chat.completions.create(model=model, **kwargs)
            return response.choices[0].message.content
        except _groq.NotFoundError as exc:
            logger.warning("Groq model '%s' unavailable (%s); trying next fallback", model, exc)
            last_exc = exc
            continue
        except Exception as exc:
            raise _handle_groq_error(exc) from exc
    raise _handle_groq_error(last_exc if last_exc is not None else GroqAPIError("generic"))


def get_text_response(messages: list[dict], system_prompt: str) -> str:
    history = [{"role": m["role"], "content": m["content"]} for m in messages]
    history = history[-MAX_HISTORY_MESSAGES:]
    try:
        return _create_with_fallback(
            TEXT_MODELS,
            messages=[{"role": "system", "content": system_prompt}] + history,
            temperature=0.2,
            max_tokens=1500,
        )
    except GroqAPIError:
        raise
    except Exception as exc:
        raise _handle_groq_error(exc) from exc


def get_vision_response(
    question: str,
    image_b64: str,
    mime: str,
    vision_system: str,
    vision_default_q: str,
) -> str:
    try:
        return _create_with_fallback(
            VISION_MODELS,
            messages=[
                {"role": "system", "content": vision_system},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url",
                         "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                        {"type": "text", "text": question or vision_default_q},
                    ],
                },
            ],
            temperature=0.2,
            max_tokens=1500,
        )
    except GroqAPIError:
        raise
    except Exception as exc:
        raise _handle_groq_error(exc) from exc
