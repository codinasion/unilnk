from django.db import models
from django.utils.text import slugify


class CategoryModel(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_total_items(self):
        return self.itemmodel_set.count()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class ItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title} {self.category}")
        super().save(*args, **kwargs)

    def get_total_clicks(self):
        return sum([link.get_total_clicks() for link in self.linkmodel_set.all()])

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

    def increase_working_count(self):
        self.working_count += 1
        self.save()

    def increase_not_working_count(self):
        self.not_working_count += 1
        self.save()

    def get_total_clicks(self):
        return self.linkclickmodel_set.count()

    def get_domain(self):
        return ".".join(self.url.split(".")[-2:])

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"


class LinkClickModel(models.Model):
    link = models.ForeignKey(LinkModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Link Click"
        verbose_name_plural = "Link Clicks"
