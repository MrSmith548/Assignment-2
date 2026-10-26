# -*- coding: utf-8 -*-
"""重启内核并执行 EXP02 notebook，将输出嵌入后保存。"""
import os
import nbformat
from nbclient import NotebookClient

HERE = os.path.dirname(os.path.abspath(__file__))
NB = os.path.join(HERE, "20244081132_唐林_exp02.ipynb")
os.environ["CONDA_DEFAULT_ENV"] = "exp02"

nb = nbformat.read(NB, as_version=4)
client = NotebookClient(
    nb,
    timeout=600,
    kernel_name="python3",
    resources={"metadata": {"path": HERE}},
)
client.execute()

with open(NB, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)
print("executed and saved:", NB)
