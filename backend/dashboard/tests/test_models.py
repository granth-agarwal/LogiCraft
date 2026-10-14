def test_dashboard_has_no_models():
    from django.apps import apps
    assert list(apps.get_app_config("dashboard").get_models())==[]

