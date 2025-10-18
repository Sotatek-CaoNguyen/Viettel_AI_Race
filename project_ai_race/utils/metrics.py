"""Evaluation metrics helpers."""
from typing import Iterable


def accuracy(gold: Iterable[int], predictions: Iterable[int]) -> float:
    """Compute simple accuracy for binary multi-label predictions."""
    gold_list = list(gold)
    pred_list = list(predictions)
    if not gold_list:
        return 0.0
    correct = sum(1 for g, p in zip(gold_list, pred_list) if g == p)
    return correct / len(gold_list)
