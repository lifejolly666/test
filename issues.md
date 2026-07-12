# dev 分支代码问题分析

> 分析范围:`bubble_sort.py`、`quick_sort.py`、`merge_sort.py`、`insertion_sort.py`、`test_bubble_sort.py`、`test_sorts.py`
> 分析日期:2026-07-12

## 一、正确性问题

### 1. 【严重】quick_sort 对自定义比较对象会静默丢失元素

`quick_sort.py` 用三个列表推导式分桶:

```python
less = [x for x in arr if x < pivot]
equal = [x for x in arr if x == pivot]
greater = [x for x in arr if x > pivot]
```

分桶依赖 `==` 与 `<`/`>` 语义一致。如果元素只实现了 `__lt__`/`__gt__` 而未实现 `__eq__`(Python 默认按对象身份比较),那么与 pivot 键相等但不是同一对象的元素三个条件全为 False,**会被静默丢弃**。

已实测复现:对只定义 `__gt__`/`__lt__` 的 Item 对象列表 `[Item(2,'a'), Item(1,'b'), Item(2,'c')]` 排序,输入 3 个元素只返回 2 个。

**修复建议**:改为按 `<` / `>` 分桶、其余归入 equal(`equal = [x for x in arr if not (x < pivot) and not (x > pivot)]`),或改用经典原地分区实现。

### 2. 【中】quick_sort 最坏情况递归深度可能爆栈

取中间位置元素为 pivot 只能规避"已有序"退化,构造的对抗性数据仍可能使分区极度不均,递归深度达 O(n),超过 Python 默认递归上限(1000)时抛 `RecursionError`。数据量大时(如 10 万元素的恶劣分布)存在崩溃风险。

**修复建议**:改为迭代 + 显式栈,或随机选 pivot / 三数取中,并在文档中注明限制。

## 二、文档与实现不符

### 3. 【低】bubble_sort / insertion_sort 空间复杂度描述不准确

两者 docstring 均写"空间复杂度:O(1)(原地排序)",但实现第一步就 `result = arr[:]` 复制整个列表,实际额外空间为 **O(n)**。注释虽有括号说明"复制一份",但复杂度标注本身与实现矛盾,易误导读者。

### 4. 【低】quick_sort 空间复杂度描述偏乐观

docstring 写"O(log n)(递归栈)",但每层递归创建 less/equal/greater 三个新列表,实际额外空间为 **O(n)**(最坏 O(n²)),且每层对 arr 完整遍历 3 次,常数开销大。

## 三、设计与一致性问题

### 5. 【中】四个算法文件的 `__main__` 演示代码完全重复

同一份 `test_cases` 列表在 4 个文件中复制粘贴了 4 遍。新增算法或调整用例需同步改多处,违反 DRY。
**建议**:抽取公共 demo 函数,或删除 `__main__` 块只保留单元测试。

### 6. 【中】测试文件结构重复,bubble_sort 未纳入统一测试

`test_bubble_sort.py` 与 `test_sorts.py` 的用例几乎一一对应,但 `test_sorts.py` 的 `ALGORITHMS` 列表没有包含 `bubble_sort`。同一套断言维护两份。
**建议**:合并为一个参数化测试文件,`ALGORITHMS` 覆盖全部 4 种算法(稳定性用例单独标注适用算法)。

### 7. 【低】接口与内置 sorted() 不对齐

所有实现均不支持 `key=` 与 `reverse=` 参数,也没有类型注解(如 `def quick_sort(arr: list) -> list`)。作为算法演示可接受,若作为可复用库则功能不完整。

### 8. 【低】stability 测试中 Item 类比较运算符定义不完整

`test_sorts.py` 的 Item 只定义了 `__gt__` 和 `__le__`,`test_bubble_sort.py` 的 Item 只定义了 `__gt__`。依赖 Python 反射运算符的隐式回退,可读性差,且正是这种"部分实现比较协议"的写法掩盖了问题 1(quick_sort 被排除在稳定性测试之外,丢元素缺陷未被测试暴露)。

## 四、工程化问题

### 9. 【低】缺少 README、LICENSE 和 CI

仓库无 README.md(项目说明、运行方式)、无 LICENSE、无 GitHub Actions 等 CI 配置,测试只能手动运行。
**建议**:补 README;加一个最简 CI workflow(`python -m unittest discover`)。

### 10. 【低】换行符未统一

每次提交都出现 "LF will be replaced by CRLF" 警告,仓库未配置 `.gitattributes`。多人跨平台协作时易产生整文件 diff。
**建议**:添加 `.gitattributes`(如 `*.py text eol=lf`)。

### 11. 【提示】git 历史中残留过 .pyc 文件

`__pycache__/*.pyc` 曾在 `cafefc6` 被误提交,虽已在 `38f20e4` 删除并加了 .gitignore,但仍存在于历史中。体积很小无实际影响,仅作记录。

## 汇总

| # | 严重程度 | 文件 | 问题 |
|---|---|---|---|
| 1 | 严重 | quick_sort.py | 未定义 `__eq__` 的对象排序时静默丢元素(已实测复现) |
| 2 | 中 | quick_sort.py | 对抗性数据可致递归深度 O(n) 爆栈 |
| 3 | 低 | bubble_sort.py / insertion_sort.py | docstring 空间复杂度 O(1) 与实际 O(n) 不符 |
| 4 | 低 | quick_sort.py | 空间复杂度标注偏乐观,每层 3 次遍历开销大 |
| 5 | 中 | 全部算法文件 | `__main__` 演示代码重复 4 份 |
| 6 | 中 | test_*.py | 测试结构重复,bubble_sort 未纳入统一测试 |
| 7 | 低 | 全部算法文件 | 不支持 key/reverse,无类型注解 |
| 8 | 低 | test_*.py | Item 类比较协议不完整,掩盖了问题 1 |
| 9 | 低 | 仓库 | 缺 README / LICENSE / CI |
| 10 | 低 | 仓库 | 缺 .gitattributes,换行符不统一 |
| 11 | 提示 | git 历史 | .pyc 曾被误提交(已修复) |
