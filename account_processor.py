def user_account(request):
    if not request.user:
        return {'account': None}
    if request.user.is_superuser:
        return {'account': None}
    try:
        accts = request.user.useraccount_set.all()
        if accts:
            return {'account': accts[0]}
    except AttributeError:
        return {'account': None}
