# -*- coding: utf-8 -*-
"""插入排序算法实现"""

from typing import Any, Callable, Optional


def insertion_sort(arr: list, key: Optional[Callable[[Any], Any]] = None,
                   reverse: bool = False) -> list:
    """对列表进行插入排序，返回排序后的新列表（不修改原列表）。

    只依赖 < 比较，元素无需实现 __eq__。稳定排序。

    时间复杂度：最坏/平均 O(n^2)，最好 O(n)（已有序时）
    空间复杂度：O(n)（复制输入与键列表；排序过程本身为原地操作）
    """
    result = arr[:]
    keyfn = key if key is not None else (lambda x: x)
    keys = [keyfn(x) for x in result]

    def lt(a: Any, b: Any) -> bool:
        """按排序方向比较两个键：a 是否应排在 b 之前（严格）"""
        return b < a if reverse else a < b

    for i in range(1, len(result)):
        current, current_key = result[i], keys[i]
        j = i - 1
        # 将应排在 current 之后的元素依次后移，为 current 腾出插入位置
        while j >= 0 and lt(current_key, keys[j]):
            result[j + 1], keys[j + 1] = result[j], keys[j]
            j -= 1
        result[j + 1], keys[j + 1] = current, current_key
    return result
