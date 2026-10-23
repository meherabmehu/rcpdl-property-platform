import json
from functools import wraps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .data import PROJECTS, GALLERY, FAQS, PRIVACY, TERMS
from .forms import InquiryForm

def project_for(value):
    return next((p for p in PROJECTS if str(p["id"]) == str(value)), PROJECTS[0])

def page(request, screen="home", project_id=None):
    if project_id and project_id not in (1, 2):
        raise Http404
    project = project_for(project_id or request.GET.get("project"))
    context = {"screen": screen, "projects": PROJECTS, "project": project, "gallery": GALLERY,
               "media": list(zip(project["images"], project["captions"])), "form": InquiryForm(initial={"project": project["id"]})}
    if screen in ("privacy", "terms"):
        context["sections"] = PRIVACY if screen == "privacy" else TERMS
    return render(request, f"public/{screen}.html", context)

@require_POST
def inquiry(request):
    form = InquiryForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=422)
    if settings.DEBUG and request.POST.get("scenario") == "failure":
        return JsonResponse({"ok": False, "error": "Your inquiry was not sent. Your entries are kept on this screen."}, status=503)
    phone = form.cleaned_data["phone"]
    # Never persist personal inquiry content during this frontend demonstration.
    return JsonResponse({"ok": True, "project": project_for(form.cleaned_data["project"])["name"],
                         "project_id": form.cleaned_data["project"], "phone": phone[:2] + "XXX XXX" + phone[-3:]})

@require_POST
def assistant(request):
    if settings.DEBUG and request.POST.get("scenario") == "ai-unavailable":
        return JsonResponse({"ok": False}, status=503)
    text = request.POST.get("message", "")[:2000]
    p = project_for(2 if "02" in text else request.POST.get("project", 1))
    if any("\u0980" <= c <= "\u09ff" for c in text):
        answer = f'{p["bn_name"]}: {p["katha"]} কাঠা · {p["sqft"]} বর্গফুট। মোট মূল্য ৳{p["price"]}। উপলব্ধ। প্রকল্পের তথ্য জানতে সাহায্য করতে পারি।'
        if not any(word in text for word in ("01", "02", "আয়তন", "মূল্য", "কাঠা", "দাম")):
            answer = "প্রকল্পের তথ্য জানতে সাহায্য করতে পারি।"
    else:
        answer = f'{p["name"]} details: {p["katha"]} katha · {p["sqft"]} sq ft. Total price ৳{p["price"]}. Available. Dhaka · Sample location. Approved location and ownership details are pending confirmation.'
    return JsonResponse({"ok": True, "answer": answer, "project": {"name": p["name"], "katha": p["katha"], "sqft": p["sqft"], "price": p["price"]}})

def staff_access(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("staff-sign-in")
        if not request.user.is_staff or not request.session.get("demo_mfa"):
            return render(request, "staff/restricted.html", status=403)
        return view(request, *args, **kwargs)
    return wrapped

def sign_in(request):
    error = ""
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None and user.is_staff:
            login(request, user)
            request.session["demo_mfa"] = False
            return redirect("staff-mfa")
        error = "Check your username and password."
    return render(request, "staff/auth.html", {"mode": "sign-in", "error": error, "auth_page": True})

def mfa(request):
    if not request.user.is_authenticated:
        return redirect("staff-sign-in")
    mode = "recovery" if request.GET.get("recovery") else "mfa"
    error = "Invalid code" if settings.DEBUG and request.GET.get("scenario") == "invalid-code" else ""
    if request.method == "POST":
        # Demonstration checkpoint only. It is NOT a production second factor.
        code = request.POST.get("code", "").replace(" ", "")
        if settings.DEBUG and code == ("DEMO-RECOVERY" if mode == "recovery" else "123456"):
            request.session["demo_mfa"] = True
            return redirect("staff-projects")
        error = "Invalid code"
    return render(request, "staff/auth.html", {"mode": mode, "error": error, "auth_page": True})

def forgot_password(request):
    return render(request, "staff/auth.html", {"mode": "forgot", "sent": request.method == "POST", "auth_page": True})

@require_POST
def sign_out(request):
    logout(request)
    return redirect("staff-sign-in")

@staff_access
def staff(request, screen="projects", project_id=1, inquiry_id=1):
    project = project_for(project_id)
    if project_id == 0:
        project = {**project, "id": 0, "name": "", "bn_name": "", "katha": "", "sqft": "", "price": "", "location": ""}
    if screen == "restricted":
        return render(request, "staff/restricted.html", status=403)
    context = {"screen": screen, "projects": PROJECTS, "project": project, "faqs": FAQS,
               "inquiry_id": inquiry_id, "media": list(zip(project["images"], project["captions"]))}
    return render(request, f"staff/{screen}.html", context)
