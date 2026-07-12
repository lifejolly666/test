# -*- coding: utf-8 -*-
"""冒泡排序的单元测试"""

import random
import unittest

from bubble_sort import bubble_sort


class TestBubbleSort(unittest.TestCase):

    def test_normal_list(self):
        """普通乱序列表"""
        self.assertEqual(
            bubble_sort([64, 34, 25, 12, 22, 11, 90]),
            [11, 12, 22, 25, 34, 64, 90],
        )

    def test_empty_list(self):
        """空列表"""
        self.assertEqual(bubble_sort([]), [])

    def test_single_element(self):
        """单元素列表"""
        self.assertEqual(bubble_sort([42]), [42])

    def test_already_sorted(self):
        """已有序列表（触发提前退出优化）"""
        self.assertEqual(bubble_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        """完全逆序（最坏情况）"""
        self.assertEqual(bubble_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_duplicates(self):
        """含重复元素"""
        self.assertEqual(bubble_sort([2, 2, 1, 1, 3]), [1, 1, 2, 2, 3])

    def test_all_same(self):
        """所有元素相同"""
        self.assertEqual(bubble_sort([7, 7, 7, 7]), [7, 7, 7, 7])

    def test_negative_and_float(self):
        """负数与浮点数混合"""
        self.assertEqual(
            bubble_sort([-3, 1.5, 0, -0.5, 2]),
            [-3, -0.5, 0, 1.5, 2],
        )

    def test_strings(self):
        """字符串列表（按字典序）"""
        self.assertEqual(
            bubble_sort(["banana", "apple", "cherry"]),
            ["apple", "banana", "cherry"],
        )

    def test_original_not_modified(self):
        """排序不应修改原列表"""
        original = [3, 1, 2]
        bubble_sort(original)
        self.assertEqual(original, [3, 1, 2])

    def test_random_against_builtin(self):
        """随机数据与内置 sorted() 对比 100 轮"""
        random.seed(2026)
        for _ in range(100):
            data = [random.randint(-1000, 1000) for _ in range(random.randint(0, 50))]
            self.assertEqual(bubble_sort(data), sorted(data))

    def test_stability(self):
        """稳定性：相等键的元素保持原有相对顺序"""
        # 用 (键, 序号) 元组但只按键比较——借助只比较第一个字段的包装类
        class Item:
            def __init__(self, key, tag):
                self.key = key
                self.tag = tag

            def __gt__(self, other):
                return self.key > other.key

        data = [Item(2, "a"), Item(1, "b"), Item(2, "c"), Item(1, "d")]
        result = bubble_sort(data)
        self.assertEqual([(x.key, x.tag) for x in result],
                         [(1, "b"), (1, "d"), (2, "a"), (2, "c")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
