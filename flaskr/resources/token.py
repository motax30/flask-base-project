from datetime import datetime, timezone

from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_restful import Resource
from marshmallow import fields

from flaskr.models.token import TokenBlocklistModel
from flaskr.models.user import UserModel
from flaskr.schemas.token import (AccessRefreshTokenRequestSchema,
                                  AccessRefreshTokenUidResponseSchema,
                                  AccessTokenResponseSchema, MessageSchema)


@doc(description='Token API', tags=['Token'])
class TokenResource(MethodResource, Resource):

    @use_kwargs(AccessRefreshTokenRequestSchema, location=('json'))
    @marshal_with(AccessRefreshTokenUidResponseSchema, code=201)
    @marshal_with(MessageSchema, code=401)
    @doc(description='Login and generate new access and refresh token')
    def post(self, **kwargs):
        username = kwargs["username"]
        password = kwargs["password"]
        # Query your database for username and password
        user = UserModel.query.filter_by(username=username, password=password).first()
        if user is None:
            # the user was not found on the database
            return make_response({"message": "Invalid username or password"}, 401)

        # create a new token with the user id inside
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(user.id)
        return make_response({
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "uid": user.id}, 201)

    @use_kwargs(
    {
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location=('headers'))
    @marshal_with(MessageSchema, code=201)
    @doc(description='Revoke current access token')
    @jwt_required()
    def delete(self, **kwargs):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        TokenBlocklistModel(jti=jti, created_at=now).save()
        return make_response({"message": "Access token revoked or expired"}, 201)

@doc(description='Token refresher API', tags=['Token'])
class TokenRefresherResource(MethodResource, Resource):

    @use_kwargs(
    {
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [refresh_token]'
        )
    }, location=('headers'))
    @marshal_with(AccessTokenResponseSchema, code=201)
    @doc(description='Refresh current access token')
    @jwt_required(refresh=True)
    def post(self, **kwargs):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return make_response({"access_token": new_token}, 201)
