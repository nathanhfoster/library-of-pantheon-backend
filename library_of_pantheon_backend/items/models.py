from django.db.models import (
    CharField,
    SlugField,
    ForeignKey,
    CASCADE,
    ManyToManyField,
    TextField,
    BooleanField,
    TextChoices
)
from library_of_pantheon_backend.utils.models import TimeStampAbstractModel, AbstractArchivedModel, OwnerAbstractModel
from django.core.validators import MinLengthValidator
from .types import ITEM_TYPES, ARTICLE


class Category(TimeStampAbstractModel):
    name = CharField(validators=[MinLengthValidator(3)], max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name',)


class Item(TimeStampAbstractModel, AbstractArchivedModel, OwnerAbstractModel):
    name = CharField(validators=[MinLengthValidator(3)], max_length=50)
    type = CharField(validators=[MinLengthValidator(2)], max_length=20, choices=ITEM_TYPES, default=ARTICLE)
    url = CharField(validators=[MinLengthValidator(13)], max_length=250, unique=True)
    slug = SlugField(validators=[MinLengthValidator(2)], max_length=50, null=True, unique=True, blank=True)
    categories = ManyToManyField(
        Category,
        related_name='categories',
    )
    image_url = CharField(max_length=250, null=True, blank=True)
    description = TextField(max_length=1000, null=True, blank=True)
    published = BooleanField(default=True)  # to filter whether to show item in the website

    def __str__(self):
        return self.name

    def get_categories(self):
        categories = self.categories.all()
        return ",\n".join([c.name for c in categories])

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ('name',)
