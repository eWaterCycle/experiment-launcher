from ewatercycle_experiment_launcher.auth import check_auth


def test_check_auth_wrong():
    assert check_auth('wronguser', 'wrongpassword') is None
