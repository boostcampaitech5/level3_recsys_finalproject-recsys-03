import ast
import pandas as pd


def str2list(data: pd.DataFrame, columns: list) -> None:
    for col in columns:
        data[col] = data[col].apply(lambda x: ast.literal_eval(x))


def check_substring(result: str, query: str) -> bool:
    result = result.lower().replace(" ", "")
    query = query.lower().replace(" ", "")
    return result in query or query in result


def check_string(result: str, query: str) -> bool:
    result = result.lower().replace(" ", "")
    query = query.lower().replace(" ", "")
    return result == query
