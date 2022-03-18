import argparse

import numpy as np

from settings import experiments, lambdas, functions, TRANSIENT_VALUE
from statistics import response_time_blockchain, number_users_system, calculate_print_transient, mean_error
from utility import read_csv, extract_data_function, filter_lambda_status, phase_path, experiment_path, \
    filter_transient_time


def main():
    iter_functions = ['upload'] if args.transient else functions
    for exp in exp_paths:
        dict_df = read_csv(exp, iter_functions)
        print(dict_df)
        exit(1)
        for fn in iter_functions:
            df_fn = extract_data_function(dict_df, fn)
            for lambda_p in lambdas:
                df_filter = filter_lambda_status(df_fn, lambda_p)
                if args.transient:
                    calculate_print_transient(df_filter, f'{args.experiment[:-2]} - lambda {lambda_p}')
                else:
                    exp_name = exp.substitute(fn=fn).split('/')[-2]
                    print(f"\n{exp_name.upper()} - {fn.upper()} - {lambda_p}")
                    df_truncated = filter_transient_time(df_filter, np.float64(TRANSIENT_VALUE))
                    print(f'avg_response_time: {response_time_blockchain(df_truncated, np.mean)}')
                    print(f'min_response_time: {response_time_blockchain(df_truncated, np.min)}')
                    print(f'max_response_time: {response_time_blockchain(df_truncated, np.max)}')
                    print(f'median_response_time: {response_time_blockchain(df_truncated, np.median)}')
                    print(f'number of users: {number_users_system(df_truncated)}')
                    df_error = filter_lambda_status(df_fn, lambda_p, status=False)

                    if df_error.shape[0] == 0:
                        print('No errors inside the experiment')
                    else:
                        print(f'#error {df_error.shape[0]}, mean_error: {mean_error(df_error)}')


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
