from simplepam import authenticate


def check_auth(username, password, required_scopes=None):
    if authenticate(username, password):
        return {'sub': username}
    return None
