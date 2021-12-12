# Cookbook

```bash
git clone https://github.com/thiennn2/cookbook.git your_project_name
cd your_project_name

# Create a virtualenv to isolate our package dependencies locally
virtualenv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the migrations
python manage.py makemigrations
python manage.py migrate
```
## Load some test data
Now is a good time to load up some test data.
The easiest option will be to download the [ingredients.json](https://raw.githubusercontent.com/graphql-python/graphene-django/master/examples/cookbook/cookbook/ingredients/fixtures/ingredients.json) fixture and place it in 
*cookbook/ingredients/fixtures/ingredients.json*.
You can then run the following:

```bash
python manage.py loaddata ingredients

Installed 6 object(s) from 1 fixture(s)
```

## Create a superuser
```bash
python manage.py createsuperuser
```

## Demo
Now that you have a superuser, you can run the demo:
- private graphql http://localhost:8000/graphql/
- public graphql http://localhost:8000/public-graphql/

Login with public graphql:
```
mutation Login {
  login(username: "admin", password: "*******") {
    me
  }
}
```
Query ingredients with private graphql:
```
query {
  allIngredients {
    id
    name
    category {
      id
      name
      __typename
    }
    __typename
  }
}
```

## Reference
- [Adding Login Required](https://docs.graphene-python.org/projects/django/en/latest/authorization/#adding-login-required)