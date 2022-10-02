from email.policy import default
from hashlib import md5
from pyexpat import model

from django.db import models

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from graphql import GraphQLError

# Create your models here.
class URL(models.Model):
    full_url = models.URLField(unique=True)
    url_hash = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # クリック回数を増やす回数
    def clicked(self):
        self.clicks += 1

        self.save()

    # ハッシュ化されたURLを返す処理をsaveに追加
    def save(self, *args, **kwargs):
        if not self.id:
            self.url_hash = md5(self.full_url.encode()).hexdigest()[:10]

        validate = URLValidator()
        try:
            validate(self.full_url)
        except ValidationError as e:
            raise ValueError("invalid url")

        return super().save(*args, **kwargs)
