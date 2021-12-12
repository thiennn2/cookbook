from django.db.models import fields
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


from cookbook.ingredients.models import Category, Ingredient

def get_user(context):
    try:
        return context.user
    except Exception:
        raise Exception('User not found!')

# def authenticate(email, password):
#     user = User.objects.get(email=email)
#     if user.check_password(password):
#         return user
#     return None

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "is_active")
        # password = graphene.String()
        # groups = graphene.List(graphene.String)
        # user_permissions = graphene.List(graphene.String)
        # is_staff = graphene.Boolean()
        # is_active = graphene.Boolean()
        # is_superuser = graphene.Boolean()
        # last_login = graphene.String()
        # date_joined = graphene.String()

class LogInMutation(graphene.Mutation):
    me = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    @staticmethod
    def mutate(root, info, **input):
        username = input.get('username')
        password = input.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(info.context, user)
            return LogInMutation(me=user)
        return LogInMutation(me=None)

class PrivateQuery(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    me = graphene.Field(UserType)

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        print(type(info.context.user))
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None
    
    def resolve_me(self, info):
        context = info.context
        user = get_user(context)
        if not user:
            raise Exception('Not logged in!')

        return user
        

class PrivateMutation(graphene.ObjectType):
    pass

class PublicQuery(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        context = info.context
        user = get_user(context)
        if not user:
            raise Exception('Not logged in!')

        return user

class PublicMutation(graphene.ObjectType):
    login = LogInMutation.Field()


private_schema = graphene.Schema(query=PrivateQuery)
public_schema = graphene.Schema(query=PublicQuery, mutation=PublicMutation)