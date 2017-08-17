from functools import wraps

from flask import flash, redirect, url_for
from flask.ext.login import current_user


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if hasattr(current_user, 'confirmed'):
            if current_user.confirmed is False:
                flash('Please confirm your account!', 'warning')
                return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function
