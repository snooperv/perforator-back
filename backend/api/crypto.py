from uuid import uuid4


def gen_token():
    return uuid4().hex
