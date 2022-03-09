import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from settings import SIMULATION_TIME
from utility import processing, truncate_length, extract_smooth_graph


def response_time_blockchain(df: pd.DataFrame, operation) -> {}:
    data = processing(df, operation)
    return mu_confidence_interval(data)


def mu_confidence_interval(data: np.ndarray) -> {}:
    t = 1.64
    mu = np.mean(data)
    standard_deviation = np.std(data)
    M = data.shape[0]
    t_student = t * standard_deviation / np.sqrt(M)
    first_interval = mu - t_student
    second_interval = mu + t_student
    return {
        'mu': mu,
        't_student': t_student,
        'first_interval': first_interval,
        'second_interval': second_interval
    }


def number_users_system(df: pd.DataFrame) -> {}:
    throughput = processing(df, np.array, count_row=True)
    throughput /= SIMULATION_TIME
    avg_response_time = processing(df, np.mean)
    users_number = throughput * avg_response_time
    return mu_confidence_interval(users_number)


def mean_error(df: pd.DataFrame) -> {}:
    errors = processing(df, np.array, count_row=True)
    return mu_confidence_interval(errors)


def calculate_print_transient(df: pd.DataFrame, title: str) -> None:
    def _dark_subplots() -> tuple:
        plt.style.use('dark_background')
        figure, axes = plt.subplots()
        figure.patch.set_facecolor('#252526')
        axes.set_facecolor('#3c3c3c')

        return figure, axes

    num_repetition = len(df.groupby('num_run'))
    min_length = truncate_length(df, num_repetition)

    sums = np.zeros(min_length)
    for num_run in range(num_repetition):
        df_truncate = df[df['num_run'] == num_run]['time_fun'][:min_length]
        sums += df_truncate.to_numpy()

    means = np.zeros(min_length)
    for idx in range(min_length):
        means[idx] = sums[idx] / num_repetition

    smooth_data = extract_smooth_graph(means)

    fig, ax = _dark_subplots()
    fig.suptitle(title, fontsize=15)
    ax.plot(smooth_data[:60])
    plt.show()
