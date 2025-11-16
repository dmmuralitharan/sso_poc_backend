from datetime import datetime, timezone
import bcrypt
from src import db
from flask import jsonify, request
from src.models.user_model import User
from src.utils.jwt import generate_jwt_token


def register_user_controller():
    try:
        firebase_uid = request.headers.get("X-FIREBASE-UID")
        if not firebase_uid:
            return jsonify({"error": "Missing Firebase UID"}), 400

        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")  # Will be None for Google signup
        name = data.get("name")
        photo_url = data.get("photo_url")
        provider = data.get("provider")  # "password" or "google"

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 409

        hashed_password = None
        if provider == "password":
            if not password:
                return jsonify({"error": "Password required"}), 400
            # Hash password for storage
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

        # Create user
        user = User(
            firebase_uid=firebase_uid,
            email=email,
            password=hashed_password,
            name=name,
            photo_url=photo_url,
            role="user",
        )

        db.session.add(user)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "status": 1,
                    # "user": {
                    #     # "id": user.id,
                    #     # "email": user.email,
                    #     "firebase_uid": user.firebase_uid,
                    #     # "name": user.name,
                    #     # "photo_url": user.photo_url,
                    #     # "role": user.role,
                    #     # "provider": provider,
                    # },
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return (jsonify({"success": 0, "error": str(e)}), 500)


def login_user_controller():
    try:
        firebase_uid = request.headers.get("X-FIREBASE-UID")

        if not firebase_uid:
            return jsonify({"error": "Missing Firebase UID"}), 400

        # Find user in DB
        user = User.query.filter_by(firebase_uid=firebase_uid).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update last_login
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        # Create JWT
        access_token = generate_jwt_token({"user_id": user.id, firebase_uid: firebase_uid})

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "user": {
                        "id": str(user.id),
                        "firebase_uid": firebase_uid,
                        "email": user.email,
                        "name": user.name,
                        "photo_url": user.photo_url,
                        "provider": user.provider,
                        "role": user.role,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return (jsonify({"success": 0, "error": str(e)}), 500)


def fetch_user_by_uid_controller():
    try:
        uid = request.firebase_uid
        user = User.query.filter_by(firebase_uid=uid).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        return (
            jsonify(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "firebase_uid": user.firebase_uid,
                        "name": user.name,
                        "photo_url": user.photo_url,
                        "role": user.role,
                        "provider": user.provider,
                    }
                }
            ),
            200,
        )
    except Exception as e:
        return (jsonify({"success": 0, "error": str(e)}), 500)