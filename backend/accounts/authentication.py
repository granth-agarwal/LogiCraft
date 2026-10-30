from functools import lru_cache
import jwt
from jwt import PyJWKClient
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .models import Profile
from rest_framework.authentication import SessionAuthentication
from uuid import NAMESPACE_URL, uuid5

class LocalSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        if not settings.ENABLE_LOCAL_AUTH:
            return None
        result = super().authenticate(request)
        if result is None:
            return None
        user, _ = result
        profile, _ = Profile.objects.get_or_create(
            supabase_user_id=uuid5(NAMESPACE_URL, f"logicraft-local-user:{user.pk}"),
            defaults={"full_name": user.get_full_name() or user.username,
                      "role": Profile.Role.ADMIN if user.is_superuser else Profile.Role.CUSTOMER},
        )
        return profile, None

@lru_cache(maxsize=1)
def _jwks_client():
    if not settings.SUPABASE_URL:
        raise AuthenticationFailed("Supabase is not configured")
    return PyJWKClient(f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json", cache_jwk_set=True, lifespan=3600)

class SupabaseJWTAuthentication(BaseAuthentication):
    def authenticate_header(self, request):
        return "Bearer"

    def authenticate(self, request):
        header = get_authorization_header(request).split()
        if not header:
            return None
        if len(header) != 2 or header[0].lower() != b"bearer":
            raise AuthenticationFailed("Invalid Authorization header")
        try:
            token = header[1].decode()
            key = _jwks_client().get_signing_key_from_jwt(token)
            claims = jwt.decode(token, key.key, algorithms=["RS256", "ES256"], audience=settings.SUPABASE_JWT_AUDIENCE)
            user_id, email = claims["sub"], claims.get("email", "")
            metadata = claims.get("app_metadata", {})
            candidate_role = claims.get("role") if claims.get("role") in dict(Profile.Role.choices) else metadata.get("role")
            role = candidate_role if candidate_role in dict(Profile.Role.choices) else Profile.Role.CUSTOMER
            profile, _ = Profile.objects.get_or_create(supabase_user_id=user_id, defaults={"full_name": email.split("@")[0], "role": role})
            if profile.role != role and role in dict(Profile.Role.choices):
                profile.role = role
                profile.save(update_fields=["role"])
            profile.email = email
            return profile, claims
        except (jwt.PyJWTError, KeyError, ValueError) as exc:
            raise AuthenticationFailed("Invalid Supabase token") from exc
