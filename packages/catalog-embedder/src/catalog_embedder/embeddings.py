"""Thin wrapper around fastembed. No fallback: missing dep/model raises immediately."""

from __future__ import annotations

from .vectors import MODEL_NAME

_model = None


def _get_model():
    global _model
    if _model is None:
        try:
            from fastembed import TextEmbedding
        except ImportError as exc:
            raise RuntimeError(
                f"fastembed is required but not installed. Run "
                f"`uv pip install -r requirements.txt` in packages/catalog-embedder/."
            ) from exc
        _model = TextEmbedding(model_name=MODEL_NAME)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = _get_model()
    return [[float(x) for x in vec] for vec in model.embed(texts)]
