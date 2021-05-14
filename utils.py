import datetime

def modellify(obj, model):
    m = model()
    for k,v in obj.items():
        m.__setattr__(k, v)
    return m

def str_to_date(date_string):
    return datetime.datetime.strptime(date_string, '%d %B %Y')

def date_to_str(dt):
    return dt.strftime('%Y-%m-%d')

def is_new(release, last_check):
    return release.timestamp() > last_check

def dt_convert(o):
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

def idx(lst, filter):
    if not lst or len(lst) == 0:
        return -1

    try:
        return list(map(filter, lst)).index(True)
    except:
        return -1

def first(lst, filter=None):
    if not lst or len(lst) == 0:
        return None

    if filter:
        try:
            idx = list(map(filter, lst)).index(True)
        except:
            return None

        return lst[idx]

    return lst[0]

def jsondates(dct):
    for k,v in dct.items():
        if isinstance(v, datetime.date):
            dct[k] = v.strftime('%Y-%m-%dT00:00:00.000')
        elif isinstance(v, datetime.datetime):
            dct[k] = v.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        else:
            dct[k] = v

    return dct
