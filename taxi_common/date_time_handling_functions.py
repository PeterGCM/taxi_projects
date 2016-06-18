import datetime

def get_date(_timestamp):
    return datetime.datetime.fromtimestamp(_timestamp).strftime('%Y-%m-%d %H:%M:%S')