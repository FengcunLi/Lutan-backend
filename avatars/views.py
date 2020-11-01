from django.shortcuts import render
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from avatars.models import Avatar
from avatars.serializers import AvatarSerializer


class AvatarViewSet(ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    # parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, ]
