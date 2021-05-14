import json, os
from models import Userdata
from utils import modellify, dt_convert, first, idx
from const import DATA_FILE

userdata = None

def read_data():
    global userdata
    if not os.path.isfile(DATA_FILE):
        open(DATA_FILE, 'w').write('{}')

    data = json.loads(open(DATA_FILE, 'r').read())
    userdata = [modellify(i, Userdata) for i in data]

    return userdata

def write_data(data):
    output = json.dumps(
        list(map(dict, data)),
        indent=2,
        separators=(',',':'),
        default=dt_convert
    )

    open(DATA_FILE, 'w').write(output)

def get_user_data(user_id):
    user = first(userdata, lambda x: x.user_id == user_id)
    if not user:
        user = Userdata(user_id)
        userdata.append(user)
        write_data(userdata)

    return user

def save_user_data(data):
    uidx = idx(userdata, lambda x: x.user_id == data.user_id)
    if uidx == -1:
        userdata.append(data)
    else:
        userdata[uidx] = data
    write_data(userdata)
