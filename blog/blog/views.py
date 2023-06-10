from django.shortcuts import render
from articles.models import Article

def home_view(request):
    articles = Article.objects.all()
    context={
        "articles": articles
    }
    return render(request, "home_view.html", context)

import os
import json
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from martor.utils import LazyEncoder

@login_required
def markdown_uploader(request):
    """
    Makdown image upload for uploading to imgur.com
    and represent as json to markdown editor.
    """

    def is_ajax(request):
        return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"

    def image_uploader(image):
        image_types = [
            'image/png', 'image/jpg',
            'image/jpeg', 'image/pjpeg', 'image/gif'
        ]
        if image.content_type not in image_types:
            data = json.dumps({
                'status': 405,
                'error': _('Bad image format.')
            }, cls=LazyEncoder)
            return data

        if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
            to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
            data = json.dumps({
                'status': 405,
                'error': _('Maximum image file is %(size)s MB.') % {'size': to_MB}
            }, cls=LazyEncoder)
            return data

        img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
        tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
        def_path = default_storage.save(tmp_file, ContentFile(image.read()))
        img_url = os.path.join(settings.MEDIA_URL, def_path)
        print(img_url)
        data = json.dumps({
            'status': 200,
            'link': img_url,
            'name': image.name
        })
        return data
    
    if request.method == "POST" and is_ajax(request):
        if "markdown-image-upload" in request.FILES:
            image = request.FILES["markdown-image-upload"]
            response_data = image_uploader(image=image)
            return HttpResponse(response_data, content_type="application/json")
        return HttpResponse(_("Invalid request!"))
    return HttpResponse(_("Invalid request!"))