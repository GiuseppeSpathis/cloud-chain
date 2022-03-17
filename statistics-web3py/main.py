import argparse
from string import Template

import numpy as np

from settings import folders, lambdas, functions, RESULTS_GENERIC_PATH
from statistics import response_time_blockchain, number_users_system, calculate_print_transient, mean_error
from utility import read_csv, extract_data_function, filter_lambda_status, filter_transient_time


def main():
    iter_functions = ['upload'] if args.transient else functions
    dict_df = read_csv(RESULTS_CSV_PATH, iter_functions)
    for lambda_p in lambdas:
        for fn in iter_functions:
            df_fn = extract_data_function(dict_df, fn)
            df_filter = filter_lambda_status(df_fn, lambda_p)
            if args.transient:
                calculate_print_transient(df_filter, f'{args.experiment} - lambda {lambda_p}')
            else:
                print(f'avg_response_time: {response_time_blockchain(df_filter, np.mean)}')
                print(f'min_response_time: {response_time_blockchain(df_filter, np.min)}')
                print(f'max_response_time: {response_time_blockchain(df_filter, np.max)}')
                print(f'median_response_time: {response_time_blockchain(df_filter, np.median)}')
                print(f'number of users: {number_users_system(df_filter)}')
                # df_truncated = filter_transient_time(df_filter, np.float64(50.))
                df_error = filter_lambda_status(df_fn, lambda_p, status=False)
                if df_error.shape[0] == 0:
                    print('No errors inside the experiment')
                else:
                    print(f'mean_error: {mean_error(df_error)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Statistics analysis of web3py project.',
        usage='%(prog)s experiment [-t]'
    )
    parser.add_argument(
        'experiment', default='none', type=str,
        choices=folders,
        help='the name of the folder that contains the results of a simulation'
    )
    parser.add_argument(
        '-t', '--transient', default=False,
        action='store_true',
        help='calculate transient instead of steady state phase'
    )

    args = parser.parse_args()
    blockchain = args.experiment.split('_')[0]
    # TODO: review RESULTS_CSV_PATH
    RESULTS_CSV_PATH = Template('..\\web3py\\results\\transient_200_15\\polygon_ibft_4\\$folder')
    '''
    if args.transient:
        RESULTS_CSV_PATH = Template(RESULTS_GENERIC_PATH.substitute(
            phase='transient_200_15',
            experiment=args.experiment
        ))
    else:
        RESULTS_CSV_PATH = RESULTS_GENERIC_PATH.substitute(
            phase='steady_state_600_5',
            experiment=args.experiment
        )
    print(RESULTS_CSV_PATH)
    '''

    exit(main())
