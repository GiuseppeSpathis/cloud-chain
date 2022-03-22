import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from settings import SIMULATION_TIME, PLOT_DIR
from utility import processing, truncate_length, extract_smooth_graph, exists_dir, join_paths


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


def mean_error(df_all: pd.DataFrame, df_error: pd.DataFrame) -> {}:
    if df_error.shape[0] == 0:
        return {
            'mu': np.float64(0),
            't_student': np.float64(0)
        }

    errors = processing(df_error, np.array, count_row=True)
    totals = processing(df_all, np.array, count_row=True)
    percentage_error = errors / totals * 100
    return mu_confidence_interval(percentage_error)


def calculate_plot_transient(df: pd.DataFrame, title: str) -> None:
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
    plt.xlabel('# user')
    plt.ylabel('time (s)')
    plt.show()


def bar_plot_metrics(df: pd.DataFrame, labels: [], title: str, save: bool = False) -> None:
    x = np.arange(len(labels))
    width = 0.1

    fig, ax = plt.subplots(figsize=(16, 10))

    rs = [x]
    for idx in range(1, 6):
        tmp = rs[idx - 1]
        rs.append(
            [val + width for val in tmp]
        )

    rects = []
    for idx, exp in enumerate(df['exp'].unique()):
        metric_series = df[df['exp'] == exp][labels].iloc[0]
        rects.append(
            ax.bar(rs[idx], metric_series, width, label=exp)
        )

    ax.set_title(title)
    ax.set_ylabel('time (s)')

    y_max = df['max'].max() + 2.5
    ax.set_ylim(ymin=0, ymax=y_max)

    loc_ticks = [(val + (len(rects) / 2) * width) - width / 2 for val in range(len(rects[0]))]
    upper_labels = [val.upper() for val in labels]
    ax.set_xticks(loc_ticks, upper_labels)
    ax.legend(loc='upper left')

    for rect in rects:
        ax.bar_label(rect, padding=2, rotation='vertical')

    fig.tight_layout()

    if save:
        exists_dir(PLOT_DIR)
        figure_path = join_paths(PLOT_DIR, f'{title}.png')
        plt.savefig(figure_path)
    else:
        plt.show()
