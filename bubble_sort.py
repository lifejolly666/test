# -*- coding: utf-8 -*-
"""冒泡排序算法实现"""

from typing import Any, Callable, Optional


def bubble_sort(arr: list, key: Optional[Callable[[Any], Any]] = None,
                reverse: bool = False) -> list:
    """对列表进行冒泡排序，返回排序后的新列表（不修改原列表）。

    只依赖 < 比较，元素无需实现 __eq__。稳定排序。

    时间复杂度：最坏/平均 O(n^2)，最好 O(n)（已有序时提前退出）
    空间复杂度：O(n)（复制输入与键列表；排序过程本身为原地操作）
    """
    result = arr[:]
    keyfn = key if key is not None else (lambda x: x)
    keys = [keyfn(x) for x in result]

    def lt(a: Any, b: Any) -> bool:
        """按排序方向比较两个键：a 是否应排在 b 之前（严格）"""
        return b < a if reverse else a < b

    n = len(result)
    for i in range(n - 1):
        swapped = False
        # 每一轮把当前"最大"的元素冒泡到末尾，末尾 i 个元素已就位
        for j in range(n - 1 - i):
            if lt(keys[j + 1], keys[j]):
                result[j], result[j + 1] = result[j + 1], result[j]
                keys[j], keys[j + 1] = keys[j + 1], keys[j]
                swapped = True
        # 本轮没有发生交换，说明已经有序，提前退出
        if not swapped:
            break
    return result
