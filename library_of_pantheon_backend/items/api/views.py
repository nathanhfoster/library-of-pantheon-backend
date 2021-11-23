from library_of_pantheon_backend.utils.pagination import StandardResultsSetPagination
from .serializers import ItemSerializer, ItemDetailSerializer, CategorySerializer
from ..models import Item, Category
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (IsAuthenticated,)
        return super(CategoryViewSet, self).get_permissions()


class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    pagination_class = StandardResultsSetPagination
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ['slug', 'name', 'url', 'description', 'categories__name',]

    def get_queryset(self):
        if self.request.parser_context['kwargs'].get('slug', None):
            qs = super().get_queryset()
        else:
            qs = super().get_queryset().filter(published=True)
        return qs

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super(ItemViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        self.serializer_class = ItemDetailSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ItemDetailSerializer
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ItemDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)
