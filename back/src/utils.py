import os
import ast
import pandas as pd


def create_dir(path: str) -> None:
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        raise Exception(f"Creating {path} is failed !!!")


def get_first_dir(path: str) -> str:
    dirs = os.listdir(path)
    return dirs[0]


def str2list(data: pd.DataFrame, columns: list) -> None:
    for col in columns:
        data[col] = data[col].apply(lambda x: ast.literal_eval(x))