from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from .models import Message, MessageSerializer, GAVNO


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

@api_view(('POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def shit(request):
    g = GAVNO.objects.create(description='shit')
    g.save()
    return Response(data=GAVNO.objects.values_list('description'), status=201)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer




