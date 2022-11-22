#!/usr/bin/env python
# encoding: utf-8
# @author: lanyulei


from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler, Response


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    def post(self, request):
        serializer = self.get_serializer(
            data=get_request_data(request)
        )

        serializer.is_valid(raise_exception=True)  # pass the 'raise_exception' flag
        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)
        return Response(response_data)
