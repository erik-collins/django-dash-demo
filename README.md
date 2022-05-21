# django-dash-demo


This repo serves as a demo application and a simple enumeration of the steps and commands required to create a django website hosting dash and plotly figures.

If you haven't already, please read the documentation for both django and django-plotly-dash.

----------------

## Procedure

### 1. Set up your environment

a. Create a new conda environment / virtual environment for running the application.

```
conda create -n django_dash_demo python=3.8

```

b. Install the packages you're going to need

```
activate django_dash_demo
pip install dash "django>=4.0,<5.0" django_plotly_dash
```



### 2. Create a Django Project

a. Test that django installed correctly

Run **python** in the anaconda window to start the interpreter then run the below
```
import django
django.get_version()
```

Should return a verison starting 4.*

Run **quit()** to exit the interpreter and return to anaconda

```
python -m django --version
```

Should also return the same version

b. Create the demo django app. Decide what you want the project to be called, this will be the name of the python app/project.  I will call mine **analytics_dashboard**.


```
django-admin startproject analytics_dashboard
```
For an explanation of what this creates, see the django documentation.  Navigate into the directory this creates.

```
cd analytics_dashboard
```

c. Verify that this initial page runs correctly

```
python manage.py runserver
```

You will see some mention of unperformed migrations and that a development server was started at an ip address **http://127.0.0.1:8000/**. Open this in a web browser and you should see some text either saying success or an error.

You can hit CTRL+C (maybe a few times) to close the server.


### 3. Create the Django app

a. Create the django application within the project. This will also be a python project, so avoid names conflicting with packages like **django** or **dash**.  I will call mine **demo**.

```
python manage.py startapp demo
```

b. Route your new app urls.  You don't have to name this the same as your python project app, but it's good practice.

In the `urls.py` file of your project (`analytics_dashboard`), add the below line to your `urlpatterns` list.
```
path('demo/', include('demo.urls')),
```
If `include` is not available, it can be imported from `django.urls`.


c. Set up a landing page for your new demo app.

i. Add a view 

In `views.py` of your application (`demo`) add a basic response

```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the demo application index.")
```

ii. Bring that view into the application urls

Add a new file `urls.py` and add to it the following code
```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

iii. Check that your view is loaded.

You should see your new response text on http://127.0.0.1:8000/demo/.   


### 4. Run migrations

When you start the app you probably see warnings about needing migrations.  
To run database migrations run the following statement.

```
python manage.py migrate
```

To run model migrations run the following statement.
```
python manage.py makemigrations
```

### 4. Add a dash component

----------------

## Documentation

##### Django

https://docs.djangoproject.com/en/4.0/

##### Django Plotly Dash

https://django-plotly-dash.readthedocs.io/en/latest/introduction.html

##### Dash Documentation

https://dash.plotly.com/
