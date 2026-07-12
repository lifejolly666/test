# 排序算法实现

Python 实现的四种经典排序算法,接口对齐内置 `sorted()`(支持 `key=` 与 `reverse=` 参数),所有实现均返回新列表、不修改输入,且只依赖 `<` 比较(元素无需实现 `__eq__`)。

## 算法一览

| 文件 | 算法 | 时间复杂度(平均) | 稳定性 | 说明 |
|---|---|---|---|---|
| `bubble_sort.py` | 冒泡排序 | O(n²) | 稳定 | 已有序时提前退出,最好 O(n) |
| `insertion_sort.py` | 插入排序 | O(n²) | 稳定 | 小规模/近有序数据高效 |
| `merge_sort.py` | 归并排序 | O(n log n) | 稳定 | 最坏情况仍为 O(n log n) |
| `quick_sort.py` | 快速排序 | O(n log n) | 不稳定 | 迭代 + 三数取中 + 三路分区,无递归爆栈风险 |

## 使用

```python
from quick_sort import quick_sort

quick_sort([3, 1, 2])                        # [1, 2, 3]
quick_sort(["bb", "a", "ccc"], key=len)      # ['a', 'bb', 'ccc']
quick_sort([3, 1, 2], reverse=True)          # [3, 2, 1]
```

## 运行

```bash
# 演示所有算法
python demo.py

# 运行单元测试
python -m unittest discover -v
```

## 项目结构

- `bubble_sort.py` / `insertion_sort.py` / `merge_sort.py` / `quick_sort.py` — 算法实现
- `demo.py` — 统一演示入口
- `test_sorts.py` — 全部算法的统一单元测试(含稳定性、部分比较协议、恶劣数据回归用例)
- `issues.md` — 历史代码审查记录

## License

[MIT](LICENSE)
