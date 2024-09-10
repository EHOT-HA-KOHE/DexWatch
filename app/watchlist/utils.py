from watchlist.models import PoolList


def get_user_collections(request):
    if request.user:
        return PoolList.objects.filter(user=request.user).all()

    else:
        return []   # todo
