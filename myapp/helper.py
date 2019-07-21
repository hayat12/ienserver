# import base64, json
from datetime import datetime, timedelta
from django.utils import timezone
from myapp import config
import os, base64
# def fromjson(s):
#     return json.loads(s, encoding='utf-8')


def current_datetime():
    return datetime.now(tz=timezone.utc)

def current_date():
    return current_datetime().date()

# def get_ws_dir():
#     return os.path.join(config.MEDIA_ROOT, 'ws')

def ensure_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)
        
# def get_wsproduct_dir():
#     k = get_ws_dir()
#     return os.path.join(k, 'wsproduct')