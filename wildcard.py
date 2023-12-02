import re
import os
from typing import Callable, Optional
from pathlib import Path
from random import choice

TagGetter = Callable[[str], Optional[list[str]]]


def get_tags(base_dir: Path, key: str):
    for file in os.listdir(base_dir):
        if Path(file).stem.startswith(key):
            with open(os.path.join(base_dir, file), "r", encoding="utf-8") as f:
                lines = f.readlines()
            return lines
    return None


def process_prompt(prompt: str, getter: TagGetter):
    wildcard_format = re.compile(r"__([^_]+)__")
    if prompt.strip() == "":
        return prompt

    def replace(match):
        key = match.group(1)
        lines = getter(key)
        if lines is None:
            return f"__{key}__"
        return choice(lines).strip()

    return wildcard_format.sub(replace, prompt)
