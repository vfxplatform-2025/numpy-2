# -*- coding: utf-8 -*-
name = "numpy"
version = "2.2.6"
authors = ["NumPy Developers"]
description = "NumPy는 Python을 위한 고성능 수치 배열 라이브러리입니다."

variants = [
    # numpy 2.2.6 supports Python 3.10-3.13
    ["python-3.10"],
    ["python-3.11"],
    ["python-3.12"],
    ["python-3.13"],
]

build_requires = [
    # wheel 다운로드 방식이므로 빌드 도구 불필요
]

build_command = "python {root}/rezbuild.py {install}"

def commands():
    import os
    env.PATH.prepend("{root}/bin")
    py_ver = os.environ.get("REZ_PYTHON_MAJOR_VERSION", "3")
    py_minor = os.environ.get("REZ_PYTHON_MINOR_VERSION", "13")
    env.PYTHONPATH.prepend(f"{{root}}/lib/python{py_ver}.{py_minor}/site-packages")
