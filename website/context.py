from django.conf import settings
from django.utils.translation import get_language

def brand(request):
    development = settings.DEBUG and not settings.ON_VERCEL
    return {"bn": get_language() == "bn", "language": get_language(), "development_preview": development,
            "demo_scenario": request.GET.get("scenario", "") if development else ""}
