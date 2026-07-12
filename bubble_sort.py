# -*- coding: utf-8 -*-
"""冒泡排序算法实现"""


def bubble_sort(arr):
    """对列表进行冒泡排序（升序），返回排序后的新列表。

    时间复杂度：最坏/平均 O(n^2)，最好 O(n)（已有序时提前退出）
    空间复杂度：O(1)（原地排序，此处复制一份以不修改原列表）
    """
    result = arr[:]  # 复制一份，避免修改原列表
    n = len(result)
    for i in range(n - 1):
        swapped = False
        # 每一轮把当前最大的元素"冒泡"到末尾，末尾 i 个元素已就位
        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        # 本轮没有发生交换，说明已经有序，提前退出
        if not swapped:
            break
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
        print(f"原始: {case} -> 排序后: {bubble_sort(case)}")
