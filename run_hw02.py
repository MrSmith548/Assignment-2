# -*- coding: utf-8 -*-
"""重启内核并运行全部代码，将输出嵌入 notebook 后保存。"""
import os
import time

import nbformat
from nbclient import NotebookClient

NB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "20244081132_唐林_hw02.ipynb")

nb = nbformat.read(NB_PATH, as_version=4)

# 模拟“重启内核后运行全部”：清空所有单元格的执行计数与输出
for cell in nb.cells:
    if cell.cell_type == "code":
        cell.execution_count = None
        cell.outputs = []
        cell.metadata.pop("execution", None)

client = NotebookClient(
    nb,
    timeout=600,
    kernel_name="python3",
    allow_errors=False,   # 任何单元格报错即抛错，确保交付物零错误
    record_timing=True,
)
client.extra_arguments = ["--NotebookApp.iopub_data_rate_limit=1000000000"]

env = dict(os.environ)
env["CONDA_DEFAULT_ENV"] = "exp01"
env["CONDA_PREFIX"] = r"C:\Users\Administrator\.workbuddy\binaries\python\envs\exp01"

start = time.time()
client.execute(env=env)
elapsed = time.time() - start

nbformat.write(nb, NB_PATH)
print(f"OK: executed {len([c for c in nb.cells if c.cell_type=='code'])} code cells in {elapsed:.1f}s -> {NB_PATH}")
