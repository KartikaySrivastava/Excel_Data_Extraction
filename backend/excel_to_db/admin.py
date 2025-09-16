from django.contrib import admin

try:
    from .models_generated import *
    # If you want to auto-register generated models, you can:
    # for name, obj in globals().items():
    #     if isinstance(obj, type) and hasattr(obj, "_meta"):
    #         try:
    #             admin.site.register(obj)
    #         except Exception:
    #             pass
except Exception:
    pass

