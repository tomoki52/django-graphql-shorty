import graphene

from graphene_django import DjangoObjectType

from .models import URL
from django.db.models import Q


class URLType(DjangoObjectType):
    class Meta:
        model = URL


class Query(graphene.ObjectType):
    urls = graphene.List(
        URLType, url=graphene.String(), first=graphene.Int(), skip=graphene.Int()
    )

    def resolve_urls(self, info, url=None, first=None, skip=None, **kwargs):
        query_set = URL.objects.all()
        if url:
            _filter = Q(full_url__icontains=url)
            query_set = query_set.filter(_filter)

        if first:
            query_set = query_set[:first]
        if skip:
            query_set = query_set[skip:]
        return query_set


class CreateURL(graphene.Mutation):
    # Mutation後にサーバから返されるデータ
    url = graphene.Field(URLType)

    # サーバが受け入れるデータ
    class Arguments:
        full_url = graphene.String()

    def mutate(self, info, full_url):
        url = URL(full_url=full_url)
        url.save()
        return CreateURL(url=url)


class Mutation(graphene.ObjectType):
    create_url = CreateURL.Field()
