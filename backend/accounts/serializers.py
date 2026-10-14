from rest_framework import serializers
from .models import Profile
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True, required=False)
    class Meta:
        model = Profile
        fields = ["id", "supabase_user_id", "email", "full_name", "role", "phone", "warehouse", "created_at"]
        read_only_fields = ["id", "supabase_user_id", "role", "created_at"]

