from utils import jsondates

class IIterable:
    def __iter__(self):
        for k,v in self.__dict__.items():
            yield (k,v)

    def jsonly(self):
        return jsondates(dict(self))

class Userdata(IIterable):
    user_id = 0
    last_check = 0
    followed_issues = []
    language = 'it_IT'
    notifications = False

    def __init__(self, user_id=0, last_check=0, language='it_IT', followed_issues=None, notifications=False):
        self.user_id = user_id
        self.last_check = last_check
        self.language = language
        self.followed_issues = followed_issues or []
        self.notifications = notifications


