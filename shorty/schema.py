import graphene
import shortener.schema


class Query(shortener.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
