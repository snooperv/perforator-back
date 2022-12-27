import pytz
from datetime import datetime, timedelta
from .models import Tokens


def tokenCheck(request_token):
    tokens = Tokens.objects.filter(token_f=request_token)
    if len(tokens) == 0:
        return False
    else:
        utc = pytz.UTC
        token = tokens.first()
        datetime_token = (datetime.now()).replace(tzinfo=utc)

        if token.time_f < datetime_token:
            return False
    return True
