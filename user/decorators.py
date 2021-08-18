from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth import REDIRECT_FIELD_NAME


def class_login_required(cls):
    if (not isinstance(cls, type) or not issubclass(cls, View)):
        raise ImproperlyConfigured(
            "class_login_required"
            " must be applied to subclasses "
            "of View class.")
    decorator = method_decorator(login_required)
    cls.dispatch = decorator(cls.dispatch)
    return cls


def require_authenticated_permission(permission):

    def decorator(cls):
        if (not isinstance(cls, type) or not issubclass(cls, View)):
            raise ImproperlyConfigured(
                "require_authenticated_permission"
                " must be applied to subclasses "
                "of View class.")
        check_auth = (method_decorator(login_required))
        check_perm = (method_decorator(
            permission_required(permission, raise_exception=True)))
        cls.dispatch = (check_auth(check_perm(cls.dispatch)))
        return cls

    return decorator


def master_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a creator,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_master,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a creator,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
