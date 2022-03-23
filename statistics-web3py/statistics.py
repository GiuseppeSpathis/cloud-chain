import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt

from settings import SIMULATION_TIME, PLOT_DIR
from utility import processing, truncate_length, extract_smooth_graph, exists_dir, join_paths

mpl.rc('figure', max_open_warning=0)


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


def calculate_plot_transient(df: pd.DataFrame, title: str, save: bool = False) -> None:
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

    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_title(title, fontsize=24)
    ax.plot(smooth_data[:60])
    plt.xlabel('Number of user')
    plt.ylabel('Time (s)')
    plt.grid()

    if save:
        exists_dir(PLOT_DIR)
        figure_path = join_paths(PLOT_DIR, f'{title}.png')
        plt.savefig(figure_path)
    else:
        plt.show()


def bar_plot_metrics(df: pd.DataFrame, labels: [], title: str, column: str, save: bool = False) -> None:
    x = np.arange(len(labels))
    width = 0.1

    fig, ax = plt.subplots(figsize=(16, 10))

    rs = [x]
    for idx in range(1, df[column].unique().shape[0]):
        tmp = rs[idx - 1]
        rs.append(
            [val + width for val in tmp]
        )

    rects = []
    for idx, val in enumerate(df[column].unique()):
        metric_series = df[df[column] == val][labels].iloc[0]
        rects.append(
            ax.bar(rs[idx], metric_series, width, label=val)
        )

    ax.set_title(title, fontsize=24)
    ax.set_ylabel('Time (s)')

    y_max = df['max'].max() + 2.5
    ax.set_ylim(ymin=0, ymax=y_max)

    loc_ticks = [(val + (len(rects) / 2) * width) - width / 2 for val in range(len(rects[0]))]
    upper_labels = [val.upper() for val in labels]
    ax.set_xticks(loc_ticks, upper_labels)
    ax.legend(loc='upper left')

    for rect in rects:
        ax.bar_label(rect, padding=3, rotation='vertical')

    fig.tight_layout()

    if save:
        exists_dir(PLOT_DIR)
        figure_path = join_paths(PLOT_DIR, f'{title}.png')
        plt.savefig(figure_path)
    else:
        plt.show()


def bar_plot_one_metric(df: pd.DataFrame, labels: [], metric: str, title: str, save: bool = False) -> None:
    x = np.arange(len(labels))
    width = 0.1

    fig, ax = plt.subplots(figsize=(16, 10))

    rs = [x]
    for idx in range(1, df['exp'].unique().shape[0]):
        tmp = rs[idx - 1]
        rs.append(
            [val + width for val in tmp]
        )

    rects = []
    for idx, val in enumerate(df['exp'].unique()):
        metric_series = pd.Series(df[df['exp'] == val][metric])
        rects.append(
            ax.bar(rs[idx], metric_series, width, label=val)
        )

    ax.set_title(title, fontsize=24)
    ax.set_ylabel('Time (s)')
    if metric == 'mean_error':
        y_max = 100
    else:
        y_max = df[metric].max() + 7.5
    ax.set_ylim(ymin=0, ymax=y_max)

    loc_ticks = [(val + (len(rects) / 2) * width) - width / 2 for val in range(len(rects[0]))]
    ax.set_xticks(loc_ticks, labels)
    ax.legend(loc='upper left')

    for rect in rects:
        ax.bar_label(rect, padding=3, rotation='vertical')

    fig.tight_layout()

    if save:
        exists_dir(PLOT_DIR)
        figure_path = join_paths(PLOT_DIR, f'{title}.png')
        plt.savefig(figure_path)
    else:
        plt.show()
