from typing import Optional, List, Dict
import json
from pathlib import Path


def save_text(text: str, filename: str, dest: Optional[str] = None):
    """
    Write text to file
    :param text: text
    :param filename: name of file
    :param dest: destination directory
    """
    if not dest:
        dest = Path.cwd()
    path = Path(dest) / filename

    with path.open('w') as file:
        file.write(text)


def save_json(dct: List[Dict], path: str):
    """
    Write dictionary to json file
    :param dct: dictionary
    :param path: path to write news in
    """
    path = Path(path)
    with path.open('w') as file:
        json.dump(dct, file, ensure_ascii=False, indent=4, sort_keys=True)
