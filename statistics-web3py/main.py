import argparse

import numpy as np
import pandas as pd

from settings import experiments, lambdas, functions, TRANSIENT_VALUE, RESULT_DIR
from statistics import response_time_blockchain, number_users_system, calculate_plot_transient, mean_error, \
    bar_plot_metrics
from utility import read_csv, extract_data_function, filter_lambda_status, phase_path, experiment_path, \
    filter_transient_time, filter_fn_lambda, exists_dir, join_paths


def join_dataframe() -> pd.DataFrame:
    df_join = pd.DataFrame()
    for exp in exp_paths:
        dict_df = read_csv(exp, functions)
        for fn in functions:
            df_fn = extract_data_function(dict_df, fn)

            exp_name = exp.substitute(fn=fn).split('/')[-2]
            exp_mod = exp_name.rsplit('_', 1)[0].replace('_', '\n')

            df_fn['fn'] = fn
            df_fn['exp'] = exp_name
            df_fn['exp_plot'] = exp_mod
            df_join = pd.concat([df_join, df_fn], ignore_index=True)

    return filter_transient_time(df_join, np.float64(TRANSIENT_VALUE))


def metrics_dataframe() -> pd.DataFrame:
    iter_functions = ['upload'] if args.transient else functions
    df_metrics = pd.DataFrame()
    for exp in exp_paths:
        dict_df = read_csv(exp, iter_functions)
        for fn in iter_functions:
            df_fn = extract_data_function(dict_df, fn)

            exp_name = exp.substitute(fn=fn).split('/')[-2]
            exp_mod = exp_name.rsplit('_', 1)[0].replace('_', '\n')

            for lambda_p in lambdas:
                df_filter = filter_lambda_status(df_fn, lambda_p)
                if args.transient:
                    calculate_plot_transient(df_filter, f'{args.experiment[:-2]} - lambda {lambda_p}')
                else:
                    df_truncated = filter_transient_time(df_filter, np.float64(TRANSIENT_VALUE))

                    avg = response_time_blockchain(df_truncated, np.mean)
                    _min = response_time_blockchain(df_truncated, np.min)
                    _max = response_time_blockchain(df_truncated, np.max)
                    median = response_time_blockchain(df_truncated, np.median)
                    num_user = number_users_system(df_truncated)

                    df_error = filter_lambda_status(df_fn, lambda_p, status=False)
                    error = mean_error(df_filter, df_error)

                    df = pd.DataFrame({
                        'fn': [fn],
                        'exp': [exp_name],
                        'exp_plot': [exp_mod],
                        'lambda': [lambda_p],
                        'avg': [avg['mu']],
                        'avg_t_student': [avg['t_student']],
                        'min': [_min['mu']],
                        'min_t_student': [_min['t_student']],
                        'max': [_max['mu']],
                        'max_t_student': [_max['t_student']],
                        'median': [median['mu']],
                        'median_t_student': [median['t_student']],
                        'num_user': [num_user['mu']],
                        'num_user_t_student': [num_user['t_student']],
                        'mean_error': [error['mu']],
                        'mean_error_t_student': [error['t_student']]
                    })
                    df_metrics = pd.concat([df_metrics, df], ignore_index=True)

    return df_metrics


def main():
    df_metrics = metrics_dataframe()
    # df_join = join_dataframe()

    if not args.transient:
        for fn in functions:
            for lambda_p in lambdas:
                df_filter = filter_fn_lambda(df_metrics, fn, lambda_p)
                df_rounded = df_filter.round(2)
                df = df_rounded.sort_values('avg')

                title = f'{fn} - lambda {lambda_p}'
                labels = ['min', 'avg', 'median', 'max']
                bar_plot_metrics(df, labels, title, args.save)

    if args.save:
        exists_dir(RESULT_DIR)
        csv_path = join_paths(RESULT_DIR, 'metrics.csv')
        df_metrics.to_csv(csv_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Statistics analysis of web3py project.',
        usage='%(prog)s [-e EXPERIMENT] [-t] [-s]'
    )
    parser.add_argument(
        '-e', '--experiment', default='none', type=str,
        choices=experiments,
        help='the name of the folder that contains the results of a simulation'
    )
    parser.add_argument(
        '-t', '--transient', default=False,
        action='store_true',
        help='calculate transient instead of steady state phase'
    )
    parser.add_argument(
        '-s', '--save', default=False,
        action='store_true',
        help='save metrics csv and plot'
    )

    args = parser.parse_args()
    blockchain = args.experiment.split('_')[0]
    phase_path = phase_path(args.transient)
    exp_exist, exp_paths = experiment_path(args.experiment, phase_path)

    if not exp_exist:
        print('Error with specified experiment folder...')
        exit(1)

    exit(main())
