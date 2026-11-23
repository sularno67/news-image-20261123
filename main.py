"""Entrypoint: copy the pre-rendered front page to the output directory.

Standard library only. The image (entry.png, 1024x1024) is rendered by
render.py at build time and shipped in this repository; this program
just places it where the grader expects it.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT_DIR, "entry.png"))
