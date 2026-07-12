# -*- coding: utf-8 -*-
"""快速排序算法实现"""


def quick_sort(arr):
    """对列表进行快速排序（升序），返回排序后的新列表。

    时间复杂度：平均 O(n log n)，最坏 O(n^2)（分区极度不均时）
    空间复杂度：O(log n)（递归栈，此实现另有分区列表开销）
    """
    if len(arr) <= 1:
        return arr[:]
    # 取中间元素作为基准，避免已有序输入退化为最坏情况
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)


if __name__ == "__main__":
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 1, 4, 2, 8],
        [1, 2, 3, 4, 5],   # 已有序
        [3],                # 单元素
        [],                 # 空列表
        [2, 2, 1, 1, 3],    # 含重复元素
    ]
    for case in test_cases:
        print(f"原始: {case} -> 排序后: {quick_sort(case)}")
