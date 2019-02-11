from rest_framework.response import Response


def success_response(data, message, status):

    data = {
        'status': 'Success',
        'data': data,
        'message': message
    }
    
    return Response(data, status=status)

def failure_response(data, message, status):

    data = {
        'status': 'Failure',
        'errors': data,
        'message': message
    }

    return Response(data, status=status)