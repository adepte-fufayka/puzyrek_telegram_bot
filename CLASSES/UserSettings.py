class UserSettings:
    time_zone=3
    role=0
    do_ping=True
    user_id:int
    def __init__(self, user_id, time_zone, role, do_ping):
        self.do_ping = do_ping
        self.role = role
        self.time_zone = time_zone
        self.user_id = user_id