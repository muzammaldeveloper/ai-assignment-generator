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
@limiter.limit("10/minute")
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


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("15/minute")
def login():
    """
    Authenticate a user and return JWT tokens.

    Request Body:
        - email (str): Registered email address.
        - password (str): Account password.

    Returns:
        200: Authenticated with access and refresh tokens.
        401: Invalid credentials or account not found.
        403: Account deactivated.
    """
    data = _login_schema.load(request.get_json())
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({
            "success": False,
            "error": "Unauthorized",
            "message": "Invalid email or password.",
        }), 401

    if not user.is_active:
        return jsonify({
            "success": False,
            "error": "Forbidden",
            "message": "Account deactivated.",
        }), 403

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    logger.info("User logged in | email=%s", user.email)

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "data": {
            "user": _user_response_schema.dump(user),
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Issue a new access token using a valid refresh token.

    Returns:
        200: New access token issued.
        401: Missing or invalid refresh token.
    """
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id)
    return jsonify({"success": True, "data": {"access_token": new_token}}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    """
    Return the profile of the currently authenticated user.

    Returns:
        200: User profile data.
        401: Missing or invalid access token.
        404: User no longer exists.
    """
    user = db.session.get(User, get_jwt_identity())
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404
    return jsonify({"success": True, "data": _user_response_schema.dump(user)}), 200