import os
from string import Template

import numpy as np
import pandas as pd


def experiment_path(transient: bool, experiment: str) -> Template:
    if transient:
        from settings import TRANSIENT_PATH
        phase_path = TRANSIENT_PATH
    else:
        from settings import STEADY_STATE_PATH
        phase_path = STEADY_STATE_PATH
    return Template(f'{phase_path}\\{experiment}\\$folder')


def read_csv(path: Template, functions: []) -> {}:
    dict_df = {}
    for fn in functions:
        dict_df[fn] = []
        function_path = path.substitute(folder=fn)
        for filename in os.listdir(function_path):
            dict_df[fn].append(
                pd.read_csv(os.path.join(function_path, filename))
            )
    return dict_df


def extract_data_function(dict_df: {}, fn: str) -> pd.DataFrame:
    df = pd.concat(dict_df[fn], ignore_index=True)
    return df


def filter_lambda_status(df: pd.DataFrame, lambda_p: float, status: bool = True) -> pd.DataFrame:
    return df[(df['lambda'] == lambda_p) & (df['status'] == status)]


def filter_transient_time(df: pd.DataFrame, time: np.float64) -> pd.DataFrame:
    return df[df['start_fun'] > time]


def processing(df: pd.DataFrame, operation, count_row: bool = False) -> np.ndarray:
    data = np.array([])
    num_repetition = df['num_run'].unique()
    for num_run in num_repetition:
        df_tmp = df[df['num_run'] == num_run]['time_fun']
        data = np.append(
            data,
            np.array(operation(df_tmp.shape[0] if count_row else df_tmp))
        )

    return data


def truncate_length(df: pd.DataFrame, num_repetition: int) -> int:
    lengths = np.array([], dtype=int)
    for num_run in range(num_repetition):
        lengths = np.append(
            lengths,
            df[df['num_run'] == num_run].shape[0]
        )
    return np.min(lengths)


def extract_smooth_graph(mu: np.ndarray, k: int = 10) -> np.ndarray:
    tmp = mu
    for idx in range(len(mu) - (k + 1)):
        tmp[idx] = short_term_fluctuations(idx, k, mu)
    return tmp


def short_term_fluctuations(n: int, k: int, mu: np.ndarray) -> float:
    value = .0

    if n >= k + 1:
        iterator = range(-k, k)
        divisor = (2 * k + 1)
    else:
        iterator = range(-(n - 1), (n - 1))
        divisor = (2 * n - 1)

    for idx in iterator:
        value += mu[n + idx]

    value /= divisor
    return value
