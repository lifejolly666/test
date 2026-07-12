# -*- coding: utf-8 -*-
"""排序算法统一演示入口：python demo.py"""

from bubble_sort import bubble_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort

ALGORITHMS = [bubble_sort, quick_sort, merge_sort, insertion_sort]

TEST_CASES = [
    [64, 34, 25, 12, 22, 11, 90],
    [5, 1, 4, 2, 8],
    [1, 2, 3, 4, 5],   # 已有序
    [3],                # 单元素
    [],                 # 空列表
    [2, 2, 1, 1, 3],    # 含重复元素
]


def main() -> None:
    for sort_fn in ALGORITHMS:
        print(f"=== {sort_fn.__name__} ===")
        for case in TEST_CASES:
            print(f"原始: {case} -> 排序后: {sort_fn(case)}")
        print()


if __name__ == "__main__":
    main()
