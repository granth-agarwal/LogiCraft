import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods


@ensure_csrf_cookie
@csrf_protect
@require_http_methods(["GET", "POST", "DELETE"])
def session(request):
    if not settings.ENABLE_LOCAL_AUTH:
        return JsonResponse({"detail": "Local login is disabled."}, status=404)
    if request.method == "GET":
        return JsonResponse({"authenticated": request.user.is_authenticated})
    if request.method == "DELETE":
        logout(request)
        return JsonResponse({"authenticated": False})
    try:
        data = json.loads(request.body)
        username, password = data["username"], data["password"]
        if not isinstance(username, str) or not isinstance(password, str):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        return JsonResponse({"detail": "Provide username and password."}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"detail": "Invalid username or password."}, status=401)
    login(request, user)
    return JsonResponse({"authenticated": True})
