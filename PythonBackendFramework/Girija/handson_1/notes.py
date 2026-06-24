# Task 1: Understand the Request-Response Lifecycle

""" 
DJANGO REQUEST → RESPONSE LIFECYCLE

How it works:
GET /api/courses/

1. Browser sends HTTP GET request to Django server.

2. Middleware processes the incoming request
   (authentication, sessions, security checks, etc.).

3. URL Router (urls.py) receives the request and matches
   '/api/courses/' to the appropriate view.

4. View function/class executes business logic.

5. View may interact with Models.
   Example:
   courses = Course.objects.all()

6. Model communicates with the database and retrieves data.

7. Data returns to the View.

8. View creates an HTTP response
   (JSONResponse, HttpResponse, TemplateResponse, etc.).

9. Middleware processes the outgoing response.

10. Response is sent back to the browser.

MIDDLEWARE

Middleware sits between the web server and the view.
Every request passes through middleware before reaching
the view, and every response passes through middleware
before returning to the client.


WSGI vs ASGI

WSGI (Web Server Gateway Interface)
- Traditional Python web server interface.
- Handles synchronous requests.
- Suitable for standard web applications.

ASGI (Asynchronous Server Gateway Interface)
- Supports asynchronous programming.
- Handles WebSockets, long-lived connections,
  and high-concurrency workloads.
- Required for real-time applications.

Django uses WSGI by default for most projects.

Switch to ASGI when:
- Using WebSockets
- Building chat applications
- Real-time notifications
- High-concurrency async workloads

MVC vs DJANGO MVT

Traditional MVC:

Model      -> Data and database logic
View       -> User interface
Controller -> Request handling and business logic

Django MVT:

Model    -> Same as MVC Model
View     -> Similar to MVC Controller
Template -> Similar to MVC View (UI layer)

Mapping:

MVC Model      -> Django Model
MVC View       -> Django Template
MVC Controller -> Django View
"""