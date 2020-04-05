# Todo
1. Intro about PORTS / domains

1. Create a requirements.txt file to with required package to make it easy to install the requirements  # HOMEWORK
1. Creation of a virtual environment to run the application on the server# HOMEWORK


1. Connection to the server using ssh


1. Deploy/start the application
    ```bash
    gunicorn --bind :5000 school.web:app
    ```

1. Basic introduction to CSS

1. Introduction to `url_for`:  
    1. 
        ```html
        <a href="{{url_for('students_handle')}}">Students</a>
        ```

    1. 
        ```html
        <link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
        ```

1. Introduction to `flash`:
    ```html
    {% with messages = get_flashed_messages() %}
    {% if messages %}
        <ul class=flashes>
        {% for message in messages %}
        <li>{{ message }}</li>
        {% endfor %}
        </ul>
    {% endif %}
    {% endwith %}
    ```html
