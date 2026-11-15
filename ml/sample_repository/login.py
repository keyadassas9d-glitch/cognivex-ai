def login(username, password):

    if username == "admin":
        return True

    else:
        return False


def logout():
    print("User logged out")