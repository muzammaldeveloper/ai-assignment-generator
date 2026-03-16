"""
Authentication API.

Handles user registration, login, and JWT token refresh.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from marshmallow import ValidationError

from app.extensions import db, limiter
from app.models.user import User
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema, UserResponseSchema
from app.utils.logger import get_logger

logger = get_logger(__name__)

auth_bp = Blueprint("auth", __name__)

# Schema instances
_register_schema = UserRegisterSchema()
_login_schema = UserLoginSchema()
_user_response_schema = UserResponseSchema()


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5/minute")
def register():
    """
    Register a new user.

    Request Body:
        - name (str): Display name.
        - email (str): Email address.
        - password (str): Password (min 8 chars, 1 upper, 1 lower, 1 digit).

    Returns:
        201: User created with access and refresh tokens.
        422: Validation error.
        409: Email already registered.
    """
    data = _register_schema.load(request.get_json())

    # Check if email already exists
    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify({
            "success": False,
            "error": "Conflict",
            "message": "A user with this email already exists.",
        }), 409

    # Create user
    user = User(
        name=data["name"],
        email=data["email"],
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    logger.info("User registered | email=%s", user.email)

    return jsonify({
        "success": True,
        "message": "User registered successfully.",
        "data": {
            "user": _user_response_schema.dump(user),
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
    }), 201