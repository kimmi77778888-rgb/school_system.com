"""
Custom Cloudinary storage backend using the official cloudinary SDK.
Replaces django-cloudinary-storage which is not compatible with Django 6.
"""
import os
import logging
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

logger = logging.getLogger(__name__)


@deconstructible
class MediaCloudinaryStorage(Storage):
    """
    Storage backend that uploads media files to Cloudinary.
    Compatible with Django 6.
    """

    def _open(self, name, mode='rb'):
        raise NotImplementedError("Cloudinary storage does not support reading files directly.")

    def _save(self, name, content):
        try:
            # Normalise path separators
            name = name.replace('\\', '/')
            folder, filename = os.path.split(name)
            # Use full name (without extension) as public_id so folder is embedded
            public_id = name.rsplit('.', 1)[0]  # e.g. "school/logo/myfile"

            options = {
                'use_filename': True,
                'unique_filename': True,
                'overwrite': False,
                'resource_type': 'auto',
                'public_id': public_id,
            }

            result = cloudinary.uploader.upload(content, **options)
            # Cloudinary may adjust the public_id; use what it returns
            saved_public_id = result.get('public_id', public_id)
            fmt = result.get('format', filename.rsplit('.', 1)[-1] if '.' in filename else 'jpg')
            return f"{saved_public_id}.{fmt}"
        except Exception as e:
            logger.error("Cloudinary upload failed: %s", e)
            raise

    def url(self, name):
        if not name:
            return ''
        try:
            # Already a full URL
            if name.startswith('http://') or name.startswith('https://'):
                return name
            # Normalise separators
            name = name.replace('\\', '/')
            # Strip extension to get public_id
            public_id = name.rsplit('.', 1)[0]
            return cloudinary.CloudinaryImage(public_id).build_url(secure=True)
        except Exception as e:
            logger.warning("Cloudinary url() failed for '%s': %s", name, e)
            return ''

    def exists(self, name):
        try:
            name = name.replace('\\', '/')
            public_id = name.rsplit('.', 1)[0]
            cloudinary.api.resource(public_id)
            return True
        except Exception:
            return False

    def delete(self, name):
        try:
            name = name.replace('\\', '/')
            public_id = name.rsplit('.', 1)[0]
            cloudinary.uploader.destroy(public_id)
        except Exception:
            pass

    def size(self, name):
        try:
            name = name.replace('\\', '/')
            public_id = name.rsplit('.', 1)[0]
            info = cloudinary.api.resource(public_id)
            return info.get('bytes', 0)
        except Exception:
            return 0
