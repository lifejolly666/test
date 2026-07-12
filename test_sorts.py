# -*- coding: utf-8 -*-
"""快速排序、归并排序、插入排序的单元测试"""

import random
import unittest

from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort

ALGORITHMS = [quick_sort, merge_sort, insertion_sort]


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
            expected = sorted(data)
            self.check_all(data, expected)

    def test_stability_merge_and_insertion(self):
        """稳定性：归并与插入排序应保持相等键的相对顺序"""
        class Item:
            def __init__(self, key, tag):
                self.key = key
                self.tag = tag

            def __gt__(self, other):
                return self.key > other.key

            def __le__(self, other):
                return self.key <= other.key

        for sort_fn in (merge_sort, insertion_sort):
            with self.subTest(algorithm=sort_fn.__name__):
                data = [Item(2, "a"), Item(1, "b"), Item(2, "c"), Item(1, "d")]
                result = sort_fn(data)
                self.assertEqual([(x.key, x.tag) for x in result],
                                 [(1, "b"), (1, "d"), (2, "a"), (2, "c")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
