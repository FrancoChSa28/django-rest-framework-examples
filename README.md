### Django REST API

## Set up the environment

# 1. Create an virtual environment
python3 -m venv venv 

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Install the requirements
pip install -r requirements.txt

# 4. Apply the migrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver

# Note: 
- We are using SQLite as the database.
- To create REST API, we are using Django REST Framework.

## Important Links:
# 1. Django REST Framework
- https://www.django-rest-framework.org/
- https://www.django-rest-framework.org/tutorial/quickstart/
- https://www.django-rest-framework.org/api-guide/serializers/
- https://www.django-rest-framework.org/api-guide/permissions/
- https://www.django-rest-framework.org/api-guide/generic-views/
- https://www.django-rest-framework.org/api-guide/viewsets/
- https://www.django-rest-framework.org/api-guide/routers/
- https://www.django-rest-framework.org/api-guide/relations/
- https://www.django-rest-framework.org/api-guide/fields/
- https://www.django-rest-framework.org/api-guide/validators/
- https://www.django-rest-framework.org/api-guide/fields/#core-arguments
- https://www.django-rest-framework.org/api-guide/fields/#serializer-fields
- https://www.django-rest-framework.org/api-guide/fields/#core-arguments
# 2. Django
- https://docs.djangoproject.com/en/3.1/
- https://docs.djangoproject.com/en/3.1/topics/db/models/
- https://docs.djangoproject.com/en/3.1/topics/db/queries/
- https://docs.djangoproject.com/en/3.1/topics/db/aggregation/
- https://docs.djangoproject.com/en/3.1/topics/db/transactions/
- https://docs.djangoproject.com/en/3.1/topics/db/managers/
- https://docs.djangoproject.com/en/3.1/topics/db/optimization/
- https://docs.djangoproject.com/en/3.1/topics/db/multi-db/
- https://docs.djangoproject.com/en/3.1/topics/db/sql/
- https://docs.djangoproject.com/en/3.1/topics/db/migrations/
- https://docs.djangoproject.com/en/3.1/topics/db/queries/