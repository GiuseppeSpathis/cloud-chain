import argparse

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from settings import experiments, lambdas, functions, TRANSIENT_VALUE
from statistics import response_time_blockchain, number_users_system, calculate_print_transient, mean_error
from utility import read_csv, extract_data_function, filter_lambda_status, phase_path, experiment_path, \
    filter_transient_time, filter_fn_lambda


def main():
    iter_functions = ['upload'] if args.transient else functions
    metrics_df = pd.DataFrame()
    for exp in exp_paths:
        dict_df = read_csv(exp, iter_functions)
        for fn in iter_functions:
            df_fn = extract_data_function(dict_df, fn)
            for lambda_p in lambdas:
                df_filter = filter_lambda_status(df_fn, lambda_p)
                if args.transient:
                    calculate_print_transient(df_filter, f'{args.experiment[:-2]} - lambda {lambda_p}')
                else:
                    exp_name = exp.substitute(fn=fn).split('/')[-2]
                    # print(f"\n{exp_name.upper()} - {fn.upper()} - {lambda_p}")

                    df_truncated = filter_transient_time(df_filter, np.float64(TRANSIENT_VALUE))

                    avg = response_time_blockchain(df_truncated, np.mean)
                    _min = response_time_blockchain(df_truncated, np.min)
                    _max = response_time_blockchain(df_truncated, np.max)
                    median = response_time_blockchain(df_truncated, np.median)
                    num_user = number_users_system(df_truncated)

                    df_error = filter_lambda_status(df_fn, lambda_p, status=False)
                    if df_error.shape[0] == 0:
                        error = {
                            'mu': np.float64(0),
                            't_student': np.float64(0)
                        }
                    else:
                        error = mean_error(df_filter, df_error)

                    exp_mod = exp_name.rsplit('_', 1)[0].replace('_', '\n')
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
                    metrics_df = pd.concat([metrics_df, df], ignore_index=True)
    '''
    for fn in functions:
        for lambda_p in lambdas:
            title = f'{fn} - lambda {lambda_p}'
            df = filter_fn_lambda(metrics_df, fn, lambda_p)x
            df.plot(
                kind='bar',
                title=title,
                x='exp_plot',
                y=['min', 'median', 'avg', 'max'],
                rot=0,
                figsize=(8, 8)
            )
            plt.xlabel('')
            plt.ylabel('time (s)')
            # plt.show()
            '''
    for exp in exp_paths:
        dict_df = read_csv(exp, iter_functions)
        for fn in iter_functions:
            df_fn = extract_data_function(dict_df, fn)
            for lambda_p in lambdas:
                df_fn[fn] = fn



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Statistics analysis of web3py project.',
        usage='%(prog)s [-e EXPERIMENT] [-t]'
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

    args = parser.parse_args()
    blockchain = args.experiment.split('_')[0]
    phase_path = phase_path(args.transient)
    exp_exist, exp_paths = experiment_path(args.experiment, phase_path)

    if not exp_exist:
        print('Error with specified experiment folder...')
        exit(1)

    exit(main())
