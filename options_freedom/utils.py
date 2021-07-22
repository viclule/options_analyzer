from typing import Text, List

from os import listdir
from os.path import isfile, join
import pathlib


def files_in_path(path: Text) -> List[Text]:
    path = pathlib.Path.cwd().joinpath(path)
    return [f for f in listdir(path) if isfile(join(path, f)) and f[-3:] == "csv"]
