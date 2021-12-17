import os

from django.conf import settings
from django.core.exceptions import AppRegistryNotReady

DEFAULT_CONFIG = getattr(
    settings,
    "TINYMCE_DEFAULT_CONFIG",
    {
        "theme": "silver",
        "height": 500,
        "menubar": False,
        "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
        "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
        "code,help,wordcount",
        "toolbar": "undo redo | formatselect | image |"
        "bold italic backcolor | alignleft aligncenter "
        "alignright alignjustify | bullist numlist outdent indent | "
        "removeformat | help",
        "image_caption": True,
        "menubar": 'insert',
        "selector": 'textarea',
        "image_title": True,
        "automatic_uploads": True,
        "file_picker_types": 'image',
        "file_picker_callback": 'tinymce.file_picker_callback',
        "images_upload_handler": 'tinymce.images_upload_handler',
        "images_upload_url": 'tinymce/upload_image/',
        "images_upload_base_path": 'media/',
        "images_upload_credentials": True,
    },
)

USE_SPELLCHECKER = getattr(settings, "TINYMCE_SPELLCHECKER", False)

USE_COMPRESSOR = getattr(settings, "TINYMCE_COMPRESSOR", False)

USE_EXTRA_MEDIA = getattr(settings, "TINYMCE_EXTRA_MEDIA", None)

USE_FILEBROWSER = getattr(
    settings, "TINYMCE_FILEBROWSER", "filebrowser" in settings.INSTALLED_APPS
)

JS_URL = getattr(
    settings,
    "TINYMCE_JS_URL",
    os.path.join(settings.STATIC_URL, "tinymce/tinymce.min.js"),
)
try:
    from django.contrib.staticfiles import finders

    JS_ROOT = getattr(settings, "TINYMCE_JS_ROOT",
                      finders.find("tinymce", all=False))
except AppRegistryNotReady:
    JS_ROOT = getattr(settings, "TINYMCE_JS_ROOT",
                      os.path.join(settings.STATIC_ROOT, "tinymce"))

JS_BASE_URL = JS_URL[: JS_URL.rfind("/")]
