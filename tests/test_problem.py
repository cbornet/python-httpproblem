import json

from pytest import mark
from httpproblem import problem, problem_http_response, Problem, activate_traceback, deactivate_traceback,\
    set_serialize_function


@mark.parametrize("status, title, detail, type, instance, kwargs, expected",
                  [
                      (
                              1000, 'test_title', 'test_detail', 'test_type', 'test_instance',
                              {'custom': 'test_custom'},
                              {
                                  'status': 1000, 'title': 'test_title', 'detail': 'test_detail',
                                  'type': 'test_type', 'instance': 'test_instance', 'custom': 'test_custom'
                              }
                      ),
                      (
                              None, None, None, None, None, {},
                              {}
                      ),
                      (
                              404, None, None, None, None, {},
                              {
                                  'status': 404, 'title': 'Not Found'
                              }
                      ),
                      (
                              404, None, None, 'about:blank', None, {},
                              {
                                  'status': 404, 'title': 'Not Found', 'type': 'about:blank'
                              }
                      ),
                      (
                              1000, None, None, None, None, {},
                              {
                                  'status': 1000
                              }
                      ),

                  ])
def test_problem(status, title, detail, type, instance, kwargs, expected):
    assert problem(status, title, detail, type, instance, **kwargs) == expected


@mark.parametrize("status, title, detail, type, instance, headers, kwargs, expected_body, expected_headers",
                  [
                      (
                              1000, 'test_title', 'test_detail', 'test_type', 'test_instance',
                              {'test_header_key': 'test_header_value'}, {'custom': 'test_custom'},
                              {
                                  'status': 1000, 'title': 'test_title', 'detail': 'test_detail',
                                  'type': 'test_type', 'instance': 'test_instance', 'custom': 'test_custom'
                              },
                              {
                                  'Content-Type': 'application/problem+json',
                                  'test_header_key': 'test_header_value'
                              }
                      ),
                      (
                              None, None, None, None, None, None, {},
                              {},
                              {
                                  'Content-Type': 'application/problem+json'
                              }
                      ),
                      (
                              None, None, None, None, None, {'Content-Type': 'text/plain'}, {},
                              {},
                              {
                                  'Content-Type': 'text/plain'
                              }
                      ),
                      (
                              None, None, None, None, None, {'content-type': 'text/plain'}, {},
                              {},
                              {
                                  'content-type': 'text/plain'
                              }
                      )
                  ])
def test_problem_http_response(status, title, detail, type, instance, headers, kwargs, expected_body, expected_headers):
    response = problem_http_response(status, title, detail, type, instance, headers, **kwargs)
    assert response['statusCode'] == status
    assert response['headers'] == expected_headers
    assert json.loads(response['body']) == expected_body


def test_exception_to_dict():
    deactivate_traceback()
    try:
        raise Problem(1000, 'test_title', 'test_detail', 'test_type', 'test_instance', custom='test_custom')
    except Problem as e:
        exception_as_dict = e.to_dict()
        assert exception_as_dict == {
            'status': 1000, 'title': 'test_title', 'detail': 'test_detail',
            'type': 'test_type', 'instance': 'test_instance', 'custom': 'test_custom'
        }


def test_exception_to_dict_with_global_traceback():
    activate_traceback()
    try:
        raise Problem()
    except Problem as e:
        exception_as_dict = e.to_dict()
        assert "Traceback (most recent call last):" in exception_as_dict['traceback']
        del exception_as_dict['traceback']
        assert exception_as_dict == {}


def test_exception_to_dict_with_traceback_param():
    deactivate_traceback()
    try:
        raise Problem()
    except Problem as e:
        exception_as_dict = e.to_dict(with_traceback=True)
        assert "Traceback (most recent call last):" in exception_as_dict['traceback']
        del exception_as_dict['traceback']
        assert exception_as_dict == {}


def test_exception_to_http_response():
    deactivate_traceback()
    try:
        raise Problem(1000, 'test_title', 'test_detail', 'test_type', 'test_instance', custom='test_custom')
    except Problem as e:
        response = e.to_http_response()
        assert response['statusCode'] == 1000
        assert response['headers'] == {'Content-Type': 'application/problem+json'}
        assert json.loads(response['body']) == {
            'status': 1000, 'title': 'test_title', 'detail': 'test_detail',
            'type': 'test_type', 'instance': 'test_instance', 'custom': 'test_custom'
        }


def test_exception_to_http_response_with_global_traceback():
    activate_traceback()
    try:
        raise Problem()
    except Problem as e:
        response = e.to_http_response()
        body = json.loads(response['body'])
        assert "Traceback (most recent call last):" in body['traceback']
        del body['traceback']
        assert body == {}


def test_exception_to_http_response_with_traceback_param():
    deactivate_traceback()
    try:
        raise Problem()
    except Problem as e:
        response = e.to_http_response(with_traceback=True)
        body = json.loads(response['body'])
        assert "Traceback (most recent call last):" in body['traceback']
        del body['traceback']
        assert body == {}


def test_set_serialize_function():
    set_serialize_function(lambda data: 'dummy')
    assert problem_http_response() == {
        'statusCode': None,
        'body': 'dummy',
        'headers': {'Content-Type': 'application/problem+json'},
    }


def test_str():
    actual = str(Problem(400))
    assert actual == "{'status': 400, 'title': 'Bad Request'}" or \
        actual == "{'title': 'Bad Request', 'status': 400}"


def test_repr():
    actual = repr(Problem(400))
    assert actual == "{'status': 400, 'title': 'Bad Request'}" or \
        actual == "{'title': 'Bad Request', 'status': 400}"
