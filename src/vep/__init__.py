"""Vector Embedding Playground - Interactive tool for exploring word embeddings."""

__version__ = "0.1.0"

from .vector_tools import NamedVectors, NamedVectorsLoader, similarity, normalize
from .plot import PlotDraw, WordGroups

__all__ = [
    "NamedVectors",
    "NamedVectorsLoader",
    "similarity",
    "normalize",
    "PlotDraw",
    "WordGroups",
]
