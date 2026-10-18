"""Verifier-reward diagnostics; never used to alter the training objective."""
from __future__ import annotations

from collections import defaultdict
import math


def reward_group_metrics(scores, group_ids):
    if len(scores) != len(group_ids) or not scores:
        raise ValueError("Rewards and group IDs must be nonempty and aligned")
    groups = defaultdict(list)
    for reward, group_id in zip(scores, group_ids):
        value = float(reward)
        if not math.isfinite(value):
            raise ValueError("Verifier rewards must be finite")
        groups[str(group_id)].append(value)
    values = list(groups.values())
    successful = sum(any(x > 0 for x in group) for group in values)
    stds = []
    for group in values:
        mean = sum(group) / len(group)
        stds.append(math.sqrt(sum((x - mean) ** 2 for x in group) / len(group)))
    return {
        "meta_teaching/reward_group_count": len(values),
        "meta_teaching/reward_group_size_min": min(map(len, values)),
        "meta_teaching/reward_group_size_max": max(map(len, values)),
        "meta_teaching/group_with_success_fraction": successful / len(values),
        "meta_teaching/group_without_success_fraction": 1 - successful / len(values),
        "meta_teaching/group_reward_std_mean": sum(stds) / len(stds),
        "meta_teaching/response_success_fraction": sum(float(x) > 0 for x in scores) / len(scores),
    }
