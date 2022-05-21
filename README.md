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

### 5. Set up the project for dash components

a. Configure `settings.py` in the project (`analytics_dashboard`)

i. add `'django_plotly_dash.apps.DjangoPlotlyDashConfig'` to `INSTALLED_APPS` 

ii. add `X_FRAME_OPTIONS = 'SAMEORIGIN'` somewhere in the file


iii. add `path('django_plotly_dash/', include('django_plotly_dash.urls')),` to the `urlpatterns` in `urls.py` of `analytics_dashboard`.

iv. In anaconda, run the following two commands
```
python manage.py makemigrations
python manage.py migrate
```

b. Add a new folder in your app (`demo`) for dash components called `dash_components`.

In it, add a new empty file `__init__.py`


### 6. Set up the project for HTML templates

a. Add a new folder in the `demo` project called `templates`.

b. Add a new folder within this called `common`

c. Add a new HTML file `base.html` with the following lines

```
{% block content %}
{% endblock %}
```

d. In `settings.py` add your app name (`'demo'`) to the `INSTALLED_APPS`.

### 7. Add a dash component

a. Add the dash figure py file

##### Add an existing figure

Copy it into a new file in this folder and make the following changes.

Import DjangoDash
```
from django_plotly_dash import DjangoDash
```

Change your `Dash` creation to a `DjangoDash` creation. You will give it a name in its first argument, this name is important and will be registered and referenced in HTML templates.

```
app = Dash()
```
to
```
app = DjangoDash('SimpleExample')
```

##### Create a new (example) figure

Add this code to a new file `simple_example.py`.  I will use `SimpleExample` as the component name for the rest of the demo.

```
import dash
import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')   # replaces dash.Dash

app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-color',
        options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
        value='red'
    ),
    html.Div(id='output-color'),
    dcc.RadioItems(
        id='dropdown-size',
        options=[{'label': i,
                  'value': j} for i, j in [('L','large'), ('M','medium'), ('S','small')]],
        value='medium'
    ),
    html.Div(id='output-size')

])

@app.callback(
    dash.dependencies.Output('output-color', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value')])
def callback_color(dropdown_value):
    return "The selected color is %s." % dropdown_value

@app.callback(
    dash.dependencies.Output('output-size', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value'),
     dash.dependencies.Input('dropdown-size', 'value')])
def callback_size(dropdown_color, dropdown_size):
    return "The chosen T-shirt is a %s %s one." %(dropdown_size,
                                                  dropdown_color)

```

b. Add a new template

Under `demo/templates` add a new folder for your component. I will call mine `example`.  In it add a new file `index.html` with the following content.

```
{% extends "common/base.html" %}

{%load plotly_dash%}

{% block content %} 
{% plotly_app name="SimpleExample" ratio=1 %}
{% endblock %}
```

Replace `SimpleExample` with the name in your `DjangoDash` app constructor.

c. Add a new view

i. In `views.py` add an import for your dash app such as
`from .dash_components.simple_example import app`.  

_You do not need to use the import, but the dash app is registered on construction, which needs to happen before it is rendered_

ii. Also in `views.py`, add a new method like the below code

```
def example(request, template_name, **kwargs):
    return render(request, template_name=template_name, context={})
```

iii. In `urls.py` of `demo` add the below line to `urlpatterns`

```
path('example', views.example, {'template_name': 'example/index.html'}, name='example'),
```

If you re-run your server now, you should see your application at http://127.0.0.1:8000/demo/example.

Repeat this step for as many apps as you want to load.


----------------

## Documentation

##### Django

https://docs.djangoproject.com/en/4.0/

##### Django Plotly Dash

https://django-plotly-dash.readthedocs.io/en/latest/introduction.html

##### Dash Documentation

https://dash.plotly.com/