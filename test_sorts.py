# -*- coding: utf-8 -*-
"""四种排序算法的统一单元测试"""

import random
import unittest

from bubble_sort import bubble_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort

ALGORITHMS = [bubble_sort, quick_sort, merge_sort, insertion_sort]
STABLE_ALGORITHMS = [bubble_sort, merge_sort, insertion_sort]  # quick_sort 不保证稳定


class PartialItem:
    """只实现 __lt__（未实现 __eq__）的对象，用于验证算法不依赖相等性判断"""

    def __init__(self, key, tag):
        self.key = key
        self.tag = tag

    def __lt__(self, other):
        return self.key < other.key

    def __repr__(self):
        return f"PartialItem({self.key}, {self.tag!r})"


class TestSortAlgorithms(unittest.TestCase):

    def check_all(self, data, expected):
        """对每种算法逐一断言结果"""
        for sort_fn in ALGORITHMS:
            with self.subTest(algorithm=sort_fn.__name__):
                self.assertEqual(sort_fn(data), expected)

    def test_normal_list(self):
        """普通乱序列表"""
        self.check_all([64, 34, 25, 12, 22, 11, 90],
                       [11, 12, 22, 25, 34, 64, 90])

    def test_empty_list(self):
        """空列表"""
        self.check_all([], [])

    def test_single_element(self):
        """单元素列表"""
        self.check_all([42], [42])

    def test_already_sorted(self):
        """已有序列表"""
        self.check_all([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        """完全逆序"""
        self.check_all([5, 4, 3, 2, 1], [1, 2, 3, 4, 5])

    def test_duplicates(self):
        """含重复元素"""
        self.check_all([2, 2, 1, 1, 3], [1, 1, 2, 2, 3])

    def test_all_same(self):
        """所有元素相同"""
        self.check_all([7, 7, 7, 7], [7, 7, 7, 7])

    def test_negative_and_float(self):
        """负数与浮点数混合"""
        self.check_all([-3, 1.5, 0, -0.5, 2], [-3, -0.5, 0, 1.5, 2])

    def test_strings(self):
        """字符串列表（按字典序）"""
        self.check_all(["banana", "apple", "cherry"],
                       ["apple", "banana", "cherry"])

    def test_original_not_modified(self):
        """排序不应修改原列表"""
        for sort_fn in ALGORITHMS:
            with self.subTest(algorithm=sort_fn.__name__):
                original = [3, 1, 2]
                sort_fn(original)
                self.assertEqual(original, [3, 1, 2])

    def test_random_against_builtin(self):
        """随机数据与内置 sorted() 对比 100 轮"""
        random.seed(2026)
        for _ in range(100):
            data = [random.randint(-1000, 1000) for _ in range(random.randint(0, 50))]
            self.check_all(data, sorted(data))

    def test_reverse_param(self):
        """reverse=True 降序排序"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        for sort_fn in ALGORITHMS:
            with self.subTest(algorithm=sort_fn.__name__):
                self.assertEqual(sort_fn(data, reverse=True),
                                 sorted(data, reverse=True))

    def test_key_param(self):
        """key= 自定义排序键（按绝对值）"""
        data = [-5, 3, -1, 4, -2]
        for sort_fn in ALGORITHMS:
            with self.subTest(algorithm=sort_fn.__name__):
                self.assertEqual(sort_fn(data, key=abs),
                                 sorted(data, key=abs))

    def test_key_and_reverse(self):
        """key 与 reverse 组合（按字符串长度降序）"""
        data = ["ccc", "a", "bb", "dddd"]
        for sort_fn in ALGORITHMS:
            with self.subTest(algorithm=sort_fn.__name__):
                self.assertEqual(sort_fn(data, key=len, reverse=True),
                                 sorted(data, key=len, reverse=True))

    def test_partial_comparison_no_element_loss(self):
        """回归测试（issues.md 问题 1）：只实现 __lt__ 的对象不得丢元素"""
        data = [PartialItem(2, "a"), PartialItem(1, "b"),
                PartialItem(2, "c"), PartialItem(1, "d"), PartialItem(3, "e")]
        for sort_fn in ALGORITHMS:
            with self.subTest(algorithm=sort_fn.__name__):
                result = sort_fn(data)
                self.assertEqual(len(result), len(data))
                self.assertEqual(sorted(x.tag for x in result),
                                 sorted(x.tag for x in data))
                self.assertEqual([x.key for x in result], [1, 1, 2, 2, 3])

    def test_stability(self):
        """稳定性：相等键的元素保持原有相对顺序（quick_sort 不保证，不参与）"""
        for sort_fn in STABLE_ALGORITHMS:
            with self.subTest(algorithm=sort_fn.__name__):
                data = [PartialItem(2, "a"), PartialItem(1, "b"),
                        PartialItem(2, "c"), PartialItem(1, "d")]
                result = sort_fn(data)
                self.assertEqual([(x.key, x.tag) for x in result],
                                 [(1, "b"), (1, "d"), (2, "a"), (2, "c")])

    def test_stability_with_key(self):
        """稳定性（key= 场景）：按元组首位排序，次位保持输入顺序"""
        data = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
        for sort_fn in STABLE_ALGORITHMS:
            with self.subTest(algorithm=sort_fn.__name__):
                self.assertEqual(sort_fn(data, key=lambda t: t[0]),
                                 [(1, "b"), (1, "d"), (2, "a"), (2, "c")])

    def test_large_adversarial_no_recursion_error(self):
        """回归测试（issues.md 问题 2）：大规模恶劣数据不应触发 RecursionError"""
        # 大量重复值 + 有序段拼接，构造对经典快排不友好的输入
        data = [0] * 5000 + list(range(5000)) + list(range(5000, 0, -1))
        self.assertEqual(quick_sort(data), sorted(data))


if __name__ == "__main__":
    unittest.main(verbosity=2)
