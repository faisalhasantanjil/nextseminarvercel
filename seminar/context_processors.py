from .decorators import is_organization, is_user


def permission_access(request):
    org_access = is_organization(request.user)
    user_access = is_user(request.user)
    return {'org_access': org_access, 'user_access': user_access}
