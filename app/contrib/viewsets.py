

from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet


class ModelListViewSet(
        mixins.ListModelMixin,
        GenericViewSet):
    pass


class ModelUpdateListViewSet(
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    pass


class ModelRetrieveListViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    pass


class ModelRetrieveUpdateListViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    pass


class ModelCreateRetrieveListViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    pass

