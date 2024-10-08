from functools import wraps
from flask import g,redirect,session,url_for
def login_required(f):
    # 保留f的信息
    @wraps(f)
    def inner(*args, **kwargs):
        if g.user:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return inner

