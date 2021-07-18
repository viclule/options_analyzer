from typing import Text, List

from os import listdir
from os.path import isfile, join


def files_in_path(path: Text) -> List[Text]:
    return [f for f in listdir(path) if isfile(join(path, f))]
