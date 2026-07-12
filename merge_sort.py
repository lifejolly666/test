# -*- coding: utf-8 -*-
"""归并排序算法实现"""


def merge_sort(arr):
    """对列表进行归并排序（升序），返回排序后的新列表。

    时间复杂度：最坏/平均/最好均为 O(n log n)
    空间复杂度：O(n)（归并时需要辅助空间），稳定排序
    """
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    """合并两个有序列表为一个有序列表。"""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # 使用 <= 保证相等元素保持原有顺序（稳定性）
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


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
        print(f"原始: {case} -> 排序后: {merge_sort(case)}")
