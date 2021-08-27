from ewatercycle_experiment_launcher.auth import check_basic_auth


def test_check_basic_auth_wrong():
    assert check_basic_auth('wronguser', 'wrongpassword') is None
