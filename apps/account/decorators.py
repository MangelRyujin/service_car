from django.contrib.auth.decorators import user_passes_test

def user_is_not_authenticated(function=None, login_url='/'):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated, 
        login_url=login_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator

def group_required(*group_names):
    def has_group(user):
        if not user.is_authenticated:
            return False
        
        if hasattr(user, 'groups'):
            return bool(user.groups.filter(name__in=group_names))
        
        return False
    return user_passes_test(has_group, login_url='/', redirect_field_name='next')