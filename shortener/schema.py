import graphene

from graphene_django import DjangoObjectType

from .models import URL


class URLType(DjangoObjectType):
    class Meta:
        model = URL


class Query(graphene.ObjectType):
    urls = graphene.List(URLType)

    def resolve_urls(self, info, **kwargs):
        return URL.objects.all()
