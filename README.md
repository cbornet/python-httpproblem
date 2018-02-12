
# python-httpproblem

Utility library to work with [RFC7807 Problem Details for HTTP APIs](https://tools.ietf.org/html/rfc7807).

[![Build Status][travis-image]][travis-url]
[![sonar-quality-gate][sonar-quality-gate]][sonar-url]
[![sonar-coverage][sonar-coverage]][sonar-url]
[![sonar-bugs][sonar-bugs]][sonar-url]
[![sonar-vulnerabilities][sonar-vulnerabilities]][sonar-url]

This library is very light-weight, with no external dependencies, fully-tested and works with both Python 2 and Python 3.
It has special support for [AWS lambda proxy integration output format](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format)
but it should be easy to map to any other format or framework.
Currently only JSON serialization is supported.

# Installation
```
pip install httpproblem
```

# Usage

## Build a Problem dict

The `problem()` function that can be used to build a dict with the problem fields.
```python
>>> pprint(problem(httplib.BAD_REQUEST, 'You do not have enough credit.', 'Your current balance is 30, but that costs 50.', '/account/12345/msgs/abc'))
{'detail': 'Your current balance is 30, but that costs 50.',
 'status': 400,
 'title': 'You do not have enough credit.',
 'type': '/account/12345/msgs/abc'}
```
You can also use problem extensions
```python
>>> pprint(problem(httplib.BAD_REQUEST, 'You do not have enough credit.', 'Your current balance is 30, but that costs 50.', '/account/12345/msgs/abc', balance=30, accounts=['/account/12345','/account/67890']))
{'accounts': ['/account/12345', '/account/67890'],
 'balance': 30,
 'detail': 'Your current balance is 30, but that costs 50.',
 'status': 400,
 'title': 'You do not have enough credit.',
 'type': '/account/12345/msgs/abc'}
```
As specified by [Predefined Problem Types](https://tools.ietf.org/html/rfc7807#section-4.2):

> The "about:blank" URI, when used as a problem type,
> indicates that the problem has no additional semantics beyond that of
> the HTTP status code.
  
> When "about:blank" is used, the title SHOULD be the same as the
> recommended HTTP status phrase for that code (e.g., "Not Found" for
> 404, and so on), although it MAY be localized to suit client
> preferences (expressed with the Accept-Language request header).

So if this library will automatically fill the title field if the type is not present or `about:blank`.
```python
>>> problem(404)
{'status': 404, 'title': 'Not Found'}
>>> problem(httplib.BAD_REQUEST, type='about:blank')
{'status': 400, 'type': 'about:blank', 'title': 'Bad Request'}
```

## Build a Problem HTTP response

The `problem_http_response()` function helps to build HTTP responses using the format used by the AWS lambda proxy integration.
The method will automatically fill the `Content-Type` header with `application/problem+json` and the HTTP response code with the status.
```python
>>> pprint(problem_http_response(httplib.BAD_REQUEST))
{'body': '{"status": 400, "type": "about:blank", "title": "Bad Request"}',
 'headers': {'Content-Type': 'application/problem+json'},
 'statusCode': 400}
```
You can map this to other frameworks. For instance for Flask (or Werkzeug):
```python
>>> problem = problem_http_response(400)
>>> print(flask.Response(problem['body'], status=problem['statusCode'], headers=problem['headers']))
<Response 39 bytes [400 BAD REQUEST]>
```
By default, `json.dumps` is used to serialize into JSON. This can be changed by using the `set_serialize_function`
```
>>> httpproblem.set_serialize_method(lambda data: json.dumps(data, indent=4))
>>> print(problem_http_response(400)['body'])
{
    "status": 400,
    "title": "Bad Request"
}
```
## Raise a Problem exception

The `Problem` exception class can be used to simplify the error management with try/except.
The class has methods to convert it to a Problem dict or HTTP response.
```python
>>> try:
...     raise Problem(httplib.BAD_REQUEST)
... except Problem as e:
...     print(e.to_dict())
...
{'status': 400, 'title': 'Bad Request'}
```
The `to_dict` and `to_http_response` take a `with_traceback` argument that can be used to include the traceback. You can also set it globally with the `activate_traceback()` function.
For security reasons, the default is to not include the traceback and it is recommended to not activate it in production.
```python
>>> # Add traceback by call argument
>>> try:
...     raise Problem(httplib.BAD_REQUEST)
... except Problem as e:
...     pprint(e.to_dict(with_traceback=True))
...
{'status': 400,
 'title': 'Bad Request',
 'traceback': 'Traceback (most recent call last):\n  File "<stdin>", line 2, in <module>\nProblem: {\'status\': 400, \'title\': \'Bad Request\'}\n'}
>>>
>>> # Add traceback globally
>>> httpproblem.activate_traceback()
>>> try:
...     raise Problem(httplib.BAD_REQUEST)
... except Problem as e:
...     pprint(e.to_dict())
...
{'status': 400,
 'title': 'Bad Request',
 'traceback': 'Traceback (most recent call last):\n  File "<stdin>", line 2, in <module>\nProblem: {\'status\': 400, \'title\': \'Bad Request\'}\n'}
```


[travis-image]: https://travis-ci.org/cbornet/python-httpproblem.svg?branch=master
[travis-url]: https://travis-ci.org/cbornet/python-httpproblem

[sonar-url]: https://sonarcloud.io/dashboard?id=python-httpproblem
[sonar-quality-gate]: https://sonarcloud.io/api/badges/gate?key=python-httpproblem
[sonar-coverage]: https://sonarcloud.io/api/badges/measure?key=python-httpproblem&metric=coverage
[sonar-bugs]: https://sonarcloud.io/api/badges/measure?key=python-httpproblem&metric=bugs
[sonar-vulnerabilities]: https://sonarcloud.io/api/badges/measure?key=python-httpproblem&metric=vulnerabilities
