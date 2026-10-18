import unittest

from meta_teaching.metrics import reward_group_metrics


class RewardGroupMetricsTests(unittest.TestCase):
    def test_noncontiguous_groups_after_batch_balancing(self):
        result = reward_group_metrics([0, 1, 0, 0, 0, 0], ["a", "b", "c", "a", "b", "c"])
        self.assertEqual(result["meta_teaching/reward_group_count"], 3)
        self.assertAlmostEqual(result["meta_teaching/group_with_success_fraction"], 1 / 3)
        self.assertAlmostEqual(result["meta_teaching/response_success_fraction"], 1 / 6)
        self.assertAlmostEqual(result["meta_teaching/group_reward_std_mean"], 1 / 6)

    def test_single_sample_groups_are_reported_explicitly(self):
        result = reward_group_metrics([1, 0], ["a", "b"])
        self.assertEqual(result["meta_teaching/reward_group_size_min"], 1)
        self.assertEqual(result["meta_teaching/group_reward_std_mean"], 0)
        self.assertEqual(result["meta_teaching/group_without_success_fraction"], 0.5)

    def test_invalid_rewards_are_not_silently_counted(self):
        for scores, groups in [([], []), ([1], []), ([float("nan")], ["a"])]:
            with self.assertRaises(ValueError):
                reward_group_metrics(scores, groups)
