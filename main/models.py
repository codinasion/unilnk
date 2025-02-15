from django.db import models
from django.utils.text import slugify


class CategoryModel(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.id + self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class ItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.id + self.title)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("slug", "category")
        verbose_name = "Item"
        verbose_name_plural = "Items"


class LinkModel(models.Model):
    STATUS_CHOICES = (
        ("working", "Working"),
        ("not_verified", "Not Verified"),
        ("not_working", "Not Working"),
    )

    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    url = models.URLField(max_length=255)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default="not_verified"
    )
    working_count = models.PositiveIntegerField(default=0)
    not_working_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.url

    def increase_working_count(self):
        self.working_count += 1
        self.save()

    def increase_not_working_count(self):
        self.not_working_count += 1
        self.save()

    def increase_click_count(self):
        self.click_count += 1
        self.save()

    def get_domain(self):
        return self.url.split("/")[2]

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
