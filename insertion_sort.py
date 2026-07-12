# -*- coding: utf-8 -*-
"""插入排序算法实现"""


def insertion_sort(arr):
    """对列表进行插入排序（升序），返回排序后的新列表。

    时间复杂度：最坏/平均 O(n^2)，最好 O(n)（已有序时）
    空间复杂度：O(1)（原地排序，此处复制一份以不修改原列表），稳定排序
    """
    result = arr[:]  # 复制一份，避免修改原列表
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        # 将比 current 大的元素依次后移，为 current 腾出插入位置
        while j >= 0 and result[j] > current:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
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
        print(f"原始: {case} -> 排序后: {insertion_sort(case)}")
