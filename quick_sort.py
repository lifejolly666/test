# -*- coding: utf-8 -*-
"""快速排序算法实现"""

from typing import Any, Callable, Optional


def quick_sort(arr: list, key: Optional[Callable[[Any], Any]] = None,
               reverse: bool = False) -> list:
    """对列表进行快速排序，返回排序后的新列表（不修改原列表）。

    迭代 + 三数取中 + 三路分区实现：
    - 只依赖 < 比较，元素无需实现 __eq__（相等由"既不小于也不大于"推导，不会丢元素）
    - 显式栈代替递归，恶劣数据下不会触发 RecursionError
    - 不稳定排序

    时间复杂度：平均 O(n log n)，最坏 O(n^2)（三数取中已大幅降低触发概率）
    空间复杂度：O(n)（复制输入与键列表）+ O(log n)（显式栈）
    """
    result = arr[:]
    keyfn = key if key is not None else (lambda x: x)
    keys = [keyfn(x) for x in result]

    def lt(a: Any, b: Any) -> bool:
        """按排序方向比较两个键：a 是否应排在 b 之前（严格）"""
        return b < a if reverse else a < b

    stack = [(0, len(result) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        # 三数取中：取 lo/mid/hi 三个键的中位数作为基准
        a, b, c = keys[lo], keys[(lo + hi) // 2], keys[hi]
        if lt(a, b):
            pivot = b if lt(b, c) else (c if lt(a, c) else a)
        else:
            pivot = a if lt(a, c) else (c if lt(b, c) else b)
        # 三路分区（荷兰国旗）：[lo, lt_i) < pivot，[lt_i, i) == pivot，(gt_i, hi] > pivot
        lt_i, gt_i, i = lo, hi, lo
        while i <= gt_i:
            if lt(keys[i], pivot):
                result[i], result[lt_i] = result[lt_i], result[i]
                keys[i], keys[lt_i] = keys[lt_i], keys[i]
                lt_i += 1
                i += 1
            elif lt(pivot, keys[i]):
                result[i], result[gt_i] = result[gt_i], result[i]
                keys[i], keys[gt_i] = keys[gt_i], keys[i]
                gt_i -= 1
            else:
                i += 1
        stack.append((lo, lt_i - 1))
        stack.append((gt_i + 1, hi))
    return result
