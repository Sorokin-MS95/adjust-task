from functools import wraps

from rest_framework.response import Response

import logging

logger = logging.getLogger()


def validate_query_params(serializer_cls):
    # TODO add logic to check method (GET,POST) so we can use both GET and POST params.
    # Note: GET is currently implemented.
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            try:
                serializer_obj = serializer_cls(data=request.query_params)
                if serializer_obj.is_valid():
                    request.serializer_data = serializer_obj.data
                    return function(request, *args, **kwargs)
                return Response({'errors': serializer_obj.errors,
                                 'success': False}, status=400)
            except Exception as ex:
                logger.exception(ex)
                return Response({'message': "Something went wrong and we're working on it.",
                                 'success': False}, status=500)

        return wrap

    return decorator
