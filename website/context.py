from django.conf import settings
from django.utils.translation import get_language

def brand(request):
    return {"bn": get_language() == "bn", "language": get_language(), "demo_scenario": request.GET.get("scenario", "") if settings.DEBUG else ""}
