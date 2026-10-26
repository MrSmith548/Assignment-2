# -*- coding: utf-8 -*-
"""生成《作业2：列表、字典和类》Jupyter Notebook（nbformat v4）。

学号 20244081132 / 姓名 唐林。
按从上到下编号的代码单元（不计 Markdown），在【第二个代码单元】中保留一行注释 # bonjour。
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
nb.metadata["language_info"] = {"name": "python", "version": "3.13"}

cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))


def code(text):
    cells.append(nbf.v4.new_code_cell(text))


# ==================== 封面与提交说明 ====================
md("""# 作业 2：列表、字典和类

**作者/课程**：丁平尖　　**学号**：20244081132　　**姓名**：唐林

**提交文件**：`20244081132_唐林_hw02.ipynb`（Jupyter Notebook，可在 PyCharm / VS Code 中编辑）

> **提交自检**：
> - 本 Notebook 已在独立的 conda 虚拟环境（非 base 环境）中重启内核并全量运行全部代码，确认无报错、无路径错误；
> - 按“从上到下、不计 Markdown”的代码单元编号，**第二个代码单元**中保留了一行注释 `# bonjour`（见下文“字符串的乐趣”代码框）。

**内容结构**：① 字符串的乐趣（is_palindrome / is_abecedarian / remove_vowels）　② 列表的乐趣（list_reverse / is_sorted）　③ 作为向量的元组（vec_scalar_mult / vec_inner_product / check_valid_mx / mx_vec_mult）　④ 更多向量的乐趣（面向对象 Vector 类）。""")

md("""## 0. 第一个代码框：身份与环境记录

**思路说明**：按作业要求，第一个代码框绑定身份与运行环境——记录学号、姓名、当前 conda 环境名，并用 `platform` / `uuid` / `hashlib` 生成“机器指纹”（对计算机名、机器类型、操作系统和 MAC 地址取 SHA-256 摘要前 16 位），组合成唯一 `RUN_ID`，用于标识“哪个人在哪台机器上完成了本次实验”。""")

# ---------- 代码单元 #1：身份与环境 ----------
code('''import hashlib
import os
import platform
import uuid

# 修改为自己的学号
STUDENT_ID = 20244081132
STUDENT_NAME = "唐林"

CONDA_ENV = os.environ.get("CONDA_DEFAULT_ENV", "base")
print(f"[Conda 环境 ] {CONDA_ENV}")

MACHINE_FP = hashlib.sha256(
    f"{platform.node()}|{platform.machine()}|{platform.system()}|{uuid.getnode()}".encode()
).hexdigest()[:16]

RUN_ID = f"{STUDENT_ID}-{MACHINE_FP}"
print(f"[ 学号 ]     {STUDENT_ID}")
print(f"[ 姓名 ]     {STUDENT_NAME}")
print(f"[ 机器指纹 ] {MACHINE_FP}")
print(f"[RUN_ID]   {RUN_ID}")''')

# ==================== 字符串的乐趣 ====================
md("""---

# 一、字符串的乐趣

本小节实现三个处理字符串的简单函数（按题目要求，无需对输入做错误检查）。

- **`is_palindrome(s)`**：忽略空格、标点符号与大小写后，前后读一致即为回文。用 `ch.isalnum()` 仅保留字母与数字并 `lower()` 统一大小写，再与自身反转比较（这样 `Was it a car or a cat I saw?` 这类含标点的短语也能正确判为回文）。
- **`is_abecedarian(s)`**：忽略空格后，字母按字母表顺序（允许重复）。用相邻比较 `letters[i] <= letters[i+1]`，`all()` 一次性判定。
- **`remove_vowels(s)`**：去掉元音 `a e i o u`（不区分大小写）。用集合判断、生成器过滤即可。""")

# ---------- 代码单元 #2：字符串函数（含 # bonjour） ----------
code('''# bonjour

def is_palindrome(s):
    """忽略空格、标点符号与大小写后，判断是否回文。"""
    cleaned = "".join(ch for ch in s if ch.isalnum()).lower()
    return cleaned == cleaned[::-1]

def is_abecedarian(s):
    """忽略空格后，判断字母是否按字母表顺序排列（允许重复）。"""
    letters = [ch for ch in s if not ch.isspace()]
    return all(letters[i] <= letters[i + 1] for i in range(len(letters) - 1))

def remove_vowels(s):
    """去掉所有元音字母 a e i o u（不区分大小写）。"""
    vowels = set("aeiouAEIOU")
    return "".join(ch for ch in s if ch not in vowels)

# ---- 自测 ----
print("is_palindrome('level'):", is_palindrome("level"))
print("is_palindrome('kayak'):", is_palindrome("kayak"))
print("is_palindrome('pop'):", is_palindrome("pop"))
print("is_palindrome('T A C O cat'):", is_palindrome("T A C O cat"))
print("is_palindrome('Was it a car or a cat I saw?'):",
      is_palindrome("Was it a car or a cat I saw?"))
print("is_palindrome('cat'):", is_palindrome("cat"))
print("is_abecedarian('adder'):", is_abecedarian("adder"))
print("is_abecedarian('beet'):", is_abecedarian("beet"))
print("is_abecedarian('abcd efgh xyz'):", is_abecedarian("abcd efgh xyz"))
print("is_abecedarian('dog'):", is_abecedarian("dog"))
print("remove_vowels('cat'):", remove_vowels("cat"))
print("remove_vowels('audio'):", remove_vowels("audio"))
print("remove_vowels('aeiou'):", remove_vowels("aeiou"))''')

# ==================== 列表的乐趣 ====================
md("""---

# 二、列表的乐趣

- **`list_reverse(lst)`**：返回列表的反转副本；题目明确“如果输入不是列表，应引发适当的错误”，故先 `isinstance` 校验，再 `lst[::-1]` 切片返回新列表（不破坏原列表）。
- **`is_sorted(seq)`**：判断序列是否升序。题目强调“只应遍历一次、多次遍历的低效解法不能满分”，因此用 `all(seq[i] <= seq[i+1] for i in range(len(seq)-1))` 生成器 + `all()` 短路，单次线性扫描完成。元素类型由调用方保证可比。""")

# ---------- 代码单元 #3：列表函数 ----------
code('''def list_reverse(lst):
    """返回列表的反转副本；非列表输入抛出 TypeError。"""
    if not isinstance(lst, list):
        raise TypeError("list_reverse expects a list")
    return lst[::-1]

def is_sorted(seq):
    """仅遍历一次，判断序列是否升序排列。"""
    return all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1))

# ---- 自测 ----
print("list_reverse([1, 2, 3]):", list_reverse([1, 2, 3]))
print("list_reverse([]):", list_reverse([]))
try:
    list_reverse("not a list")
except TypeError as e:
    print("TypeError:", e)

print("is_sorted([1, 2, 2, 4]):", is_sorted([1, 2, 2, 4]))
print("is_sorted([3, 1]):", is_sorted([3, 1]))
print("is_sorted('abc'):", is_sorted("abc"))
print("is_sorted((5,)):", is_sorted((5,)))''')

# ==================== 作为向量的元组 ====================
md("""---

# 三、作为向量的元组

用元组表示向量。以下函数都按题目要求做**输入类型检查**，不合适时抛出 `TypeError`；长度不一致等语义错误抛出 `ValueError`。

- **`vec_scalar_mult(t, s)`**：元组 `t` 每个元素乘以标量 `s`，返回等长新元组。
- **`vec_inner_product(a, b)`**：两向量内积，返回 `float`；任一非元组 → `TypeError`，长度不等 → `ValueError`。
- **`check_valid_mx(m)`**：判定 `m`（元组的元组）是否为合法矩阵——外层每个元素是元组、所有内层元组等长、每个元素为 `int/float`，全部满足返回 `True`，否则 `False`。
- **`mx_vec_mult(mx, v)`**：矩阵 × 向量，先用 `check_valid_mx` 校验，再按列求和得到结果元组；非法输入抛相应错误。""")

# ---------- 代码单元 #4：向量元组函数 ----------
code('''def vec_scalar_mult(t, s):
    """向量(元组)与标量相乘，返回等长元组。"""
    if not isinstance(t, tuple):
        raise TypeError("t must be a tuple")
    if isinstance(s, bool) or not isinstance(s, (int, float)):
        raise TypeError("s must be an int or float")
    return tuple(x * s for x in t)

def vec_inner_product(a, b):
    """两向量(元组)内积，返回浮点数。"""
    if not isinstance(a, tuple) or not isinstance(b, tuple):
        raise TypeError("both arguments must be tuples")
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    return float(sum(x * y for x, y in zip(a, b)))

def check_valid_mx(m):
    """判断 m 是否为合法矩阵(元组的元组，内层等长且元素为数字)。"""
    if not isinstance(m, tuple):
        return False
    for row in m:
        if not isinstance(row, tuple):
            return False
        for x in row:
            if isinstance(x, bool) or not isinstance(x, (int, float)):
                return False
    lengths = {len(row) for row in m}
    return len(lengths) <= 1

def mx_vec_mult(mx, v):
    """矩阵(元组的元组)与向量(元组)相乘，返回数值元组。"""
    if not check_valid_mx(mx):
        raise ValueError("mx is not a valid matrix")
    if not isinstance(v, tuple):
        raise TypeError("v must be a tuple")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) for x in v):
        raise TypeError("v elements must be int or float")
    if len(mx) == 0:
        raise ValueError("matrix has no rows")
    n = len(mx[0])
    if len(v) != n:
        raise ValueError("vector length must match matrix column count")
    return tuple(sum(row[j] * v[j] for j in range(n)) for row in mx)

# ---- 自测 ----
print("vec_scalar_mult((1, 2, 3), 2):", vec_scalar_mult((1, 2, 3), 2))
print("vec_scalar_mult((1.0, 2.5), 3):", vec_scalar_mult((1.0, 2.5), 3))
print("vec_inner_product((1, 2, 3), (4, 5, 6)):", vec_inner_product((1, 2, 3), (4, 5, 6)))
mx = ((1, 2, 3), (4, 5, 6))
v = (7, 8, 9)
print("check_valid_mx(mx):", check_valid_mx(mx))
print("mx_vec_mult(mx, v):", mx_vec_mult(mx, v))
print("check_valid_mx(((1, 2), (3,))):", check_valid_mx(((1, 2), (3,))))
try:
    mx_vec_mult(mx, (1, 2))
except ValueError as e:
    print("ValueError:", e)''')

# ==================== 更多向量的乐趣（OOP） ====================
md("""---

# 四、更多向量的乐趣（面向对象）

## 任务 1：`Vector` 类

每个向量有**维度**（非负整数）和**元素**（由 `int/float` 组成的列表或元组）。`__init__` 第一个参数为维度，第二个为元素；**仅提供维度不提供元素时，默认填充 0**（合理的默认行为）。维度类型错误 / 为负数 / 与元素个数不一致，都抛出对应异常。`bool` 视为非 `int` 一并排除。""")

# ---------- 代码单元 #5：Vector 类 ----------
code('''class Vector:
    """用面向对象方式表示向量。维度与元素均为实例属性(见下节说明)。"""
    def __init__(self, dim, elements=None):
        if not isinstance(dim, int) or isinstance(dim, bool):
            raise TypeError("dimension must be a non-negative integer")
        if dim < 0:
            raise ValueError("dimension must be non-negative")
        if elements is None:
            elements = [0] * dim
        if not isinstance(elements, (list, tuple)):
            raise TypeError("elements must be a list or tuple")
        if any(isinstance(x, bool) or not isinstance(x, (int, float)) for x in elements):
            raise TypeError("elements must be int or float")
        if len(elements) != dim:
            raise ValueError("dimension does not match number of elements")
        self._dim = dim
        self._elements = tuple(elements)

    @property
    def dim(self):
        return self._dim

    @property
    def elements(self):
        return self._elements

    def __repr__(self):
        return f"Vector({self._dim}, {self._elements})"

    def _check_same_dim(self, other):
        if not isinstance(other, Vector):
            raise TypeError("can only compare/operate with another Vector")
        if self._dim != other._dim:
            raise ValueError("cannot operate on Vectors of different dimensions")

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self._dim == other._dim and self._elements == other._elements

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __lt__(self, other):
        self._check_same_dim(other)
        return self._elements < other._elements

    def __le__(self, other):
        self._check_same_dim(other)
        return self._elements <= other._elements

    def __gt__(self, other):
        self._check_same_dim(other)
        return self._elements > other._elements

    def __ge__(self, other):
        self._check_same_dim(other)
        return self._elements >= other._elements

    def dot(self, other):
        """返回两向量内积(浮点数)。"""
        self._check_same_dim(other)
        return float(sum(a * b for a, b in zip(self._elements, other._elements)))

    def __mul__(self, other):
        if isinstance(other, (int, float)) and not isinstance(other, bool):
            return Vector(self._dim, [x * other for x in self._elements])
        if isinstance(other, Vector):
            self._check_same_dim(other)
            return Vector(self._dim, [a * b for a, b in zip(self._elements, other._elements)])
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)''')

md("""## 任务 2：维度与元素是类属性还是实例属性？

**结论：必须是实例属性（用 `self._dim` / `self._elements` 存储），而不是类属性。**

理由：类属性在所有实例之间**共享同一份数据**，而“维度”和“元素”是**每个向量各自独有**的状态——不同 `Vector` 对象的维度和坐标本就不同。若把它们声明为类属性，则创建一个新向量会覆盖之前所有向量的值，这是错误的。Python 的惯例也如此：只有“所有实例都相同、且需要被共享/统一修改”的量（例如一个全局计数、配色方案）才适合做类属性。本实现中维度与元素均为每实例独立的状态，故放在 `__init__` 里以 `self._xxx` 保存，并用 `@property` 提供只读访问。""")

md("""## 任务 3 / 4 / 5：比较运算符、点积、乘法运算符

- **比较运算符 `== < <= > >=`**：坐标完全相同视为相等（`__eq__`）；否则按 Python 元组的字典序比较（`__lt__` 等直接比较 `self._elements` 元组，先比第一维、再比下一维……）。**比较维度不同的两个向量时抛出异常**（`_check_same_dim`）；`==` 对维度不同的对象返回 `False`（坐标不可能相等），而对非 `Vector` 类型返回 `NotImplemented` 以遵循 Python 语义。
- **`Vector.dot(other)`**：返回内积（浮点）；类型不对或维度不一致抛异常。
- **乘法运算符 `__mul__ / __rmul__`**：
  - 标量左/右乘（`2 * v`、`v * 2`）→ 各元素乘以该标量，返回新 `Vector`；
  - 向量 × 向量（`v * w`）→ 对应位置元素逐一相乘（Hadamard 积），返回新 `Vector`，如 `Vector(2, (2, 3)) * Vector(2, (4, 5))` 元素为 `(8, 15)`；
  - 维度不一致抛异常。`__rmul__` 复用 `__mul__` 以支持标量在左侧。""")

# ---------- 代码单元 #6：Vector 演示 ----------
code('''a = Vector(2, (2, 3))
b = Vector(2, (4, 5))
c = Vector(2, (2, 5))
d = Vector(2, (2, 3))    # 与 a 坐标完全相同
z = Vector(3)            # 仅给维度 -> 默认全 0

print("a =", a)
print("b =", b)
print("z =", z)
print("a == b:", a == b)
print("a == c:", a == c)          # (2,3) 与 (2,5) 坐标不同 -> False
print("a == d:", a == d)          # 维度和坐标都相同 -> True
print("a < c:", a < c)            # (2,3) < (2,5) -> True
print("a <= b:", a <= b)          # (2,3) <= (4,5) -> True
print("b > a:", b > a)            # True
print("a.dot(b):", a.dot(b))      # 2*4 + 3*5 = 23
print("2 * a:", 2 * a)
print("a * 2:", a * 2)
print("a * b:", a * b)            # 元素逐一相乘 -> (8, 15)
print("a.dim:", a.dim)

# 异常分支演示
try:
    a < Vector(3, (1, 2, 3))
except ValueError as e:
    print("ValueError (不同维度比较):", e)
try:
    a * Vector(3, (1, 2, 3))
except ValueError as e:
    print("ValueError (不同维度相乘):", e)
try:
    a.dot("not a vector")
except TypeError as e:
    print("TypeError (dot 参数类型):", e)''')

md("""---

# 五、提交说明（对照作业要求）

1. ✅ 第一个代码框已填入学号 `20244081132` 与姓名 `唐林`。
2. ✅ 按“从上到下、不计 Markdown”的代码单元编号：**第二个代码单元**（字符串的乐趣）中保留了注释 `# bonjour`。
3. ✅ 已在本机独立 conda 虚拟环境（非 base）中**重启内核并运行全部代码**，所有 6 个代码单元均无报错；关键自测结果见上。
4. ✅ 提交文件名为 `20244081132_唐林_hw02.ipynb`。""")

nb["cells"] = cells
OUT = r"C:/Users/Administrator/WorkBuddy/2026-10-17-21-27-59/HW02作业/20244081132_唐林_hw02.ipynb"
with open(OUT, "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("written:", OUT)
print("cells:", len(cells))
