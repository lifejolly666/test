# -*- coding: utf-8 -*-
"""归并排序算法实现"""

from typing import Any, Callable, Optional


def merge_sort(arr: list, key: Optional[Callable[[Any], Any]] = None,
               reverse: bool = False) -> list:
    """对列表进行归并排序，返回排序后的新列表（不修改原列表）。

    只依赖 < 比较，元素无需实现 __eq__。稳定排序。

    时间复杂度：最坏/平均/最好均为 O(n log n)
    空间复杂度：O(n)（归并辅助空间与切片复制）
    """
    keyfn = key if key is not None else (lambda x: x)

    def goes_first(a: Any, b: Any) -> bool:
        """a 是否应排在 b 之前或与其并列（相等时取左侧元素，保证稳定性）"""
        ka, kb = keyfn(a), keyfn(b)
        return not (ka < kb) if reverse else not (kb < ka)

    def sort(items: list) -> list:
        if len(items) <= 1:
            return items[:]
        mid = len(items) // 2
        left = sort(items[:mid])
        right = sort(items[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if goes_first(left[i], right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    return sort(arr)
