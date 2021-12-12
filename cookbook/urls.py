from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene.types import schema
from graphene_django.views import GraphQLView

from cookbook.views import PrivateGraphQLView, PublicGraphQLView
from cookbook.schema import public_schema, private_schema


urlpatterns = [
    path("admin/", admin.site.urls),
    path("public-graphql/", csrf_exempt(PublicGraphQLView.as_view(graphiql=True, schema=public_schema))),
    path("graphql/", csrf_exempt(PrivateGraphQLView.as_view(graphiql=True, schema=private_schema))),
]
