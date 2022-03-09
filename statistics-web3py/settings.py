SIMULATION_TIME = 300

functions = [
    'cloud_sla_creation_activation',
    'read',
    'upload',
    'delete',
    'file_check_undeleted_file',
    'another_file_upload',
    'read_deny_lost_file_check',
    'another_file_upload_read',
    'corrupted_file_check'
]

lambdas = [
    0.5,
    1.0,
    2.0
]

folders = [
    'polygon_pos_4',
    'polygon_ibft_4',
    'besu_qbft_4',
    'besu_ibft_4',
    'besu_clique_4',
    'go-quorum_qbft_4',
    'go-quorum_ibft_4'
    'go-quorum_raft_4'
]
