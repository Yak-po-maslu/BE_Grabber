from asgiref.sync import sync_to_async

from ads.models import Ad, AdView
from services.get_client_ip import get_client_ip


async def increase_count_views_ip(request, ad_id, ad):
    ip = get_client_ip(request)


    view_exists = await sync_to_async(lambda: AdView.objects.filter(ad_id=ad_id, ip_address=ip).exists())()
    if not view_exists:
        await sync_to_async(AdView.objects.create)(ad=ad, ip_address=ip)
        ad.views += 1
        await sync_to_async(ad.save)()