from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Member, db
from . import members_bp
from app.extensions import limiter, cache
from app.utils.utils import encode_token, token_required
from .schemas import member_schema, members_schema, login_schema

# -----------------------
# LOGIN / TOKEN
# -----------------------
@members_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials.email
        password = credentials.password
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Member).where(Member.email == email)
    member = db.session.execute(query).scalars().first()

    if member and member.password == password:
        token = encode_token(member.id)
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "token": token
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# -----------------------
# CREATE MEMBER
# -----------------------
@members_bp.route('/', methods=['POST'])
def create_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check for existing email
    query = select(Member).where(Member.email == member_data.email)
    existing_member = db.session.execute(query).scalars().first()
    if existing_member:
        return jsonify({"error": "Email already exists."}), 400

    # You can use member_data directly, or create a new instance
    new_member = Member(
        name=member_data.name,
        email=member_data.email,
        DOB=member_data.DOB,
        password=member_data.password
    )

    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member), 201

# -----------------------
# GET ALL MEMBERS
# -----------------------
@members_bp.route('/', methods=['GET'])
@limiter.limit("3 per hour")
def get_members():
    all_members = db.session.execute(select(Member)).scalars().all()
    return members_schema.jsonify(all_members)

# -----------------------
# GET MEMBER BY ID
# -----------------------
@members_bp.route('/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_member(id):
    member = db.session.get(Member, id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    return member_schema.jsonify(member)

# -----------------------
# UPDATE MEMBER
# -----------------------
@members_bp.route('/<int:id>', methods=['PUT'])
def update_member(id):
    member = db.session.get(Member, id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    try:
        updated_data = member_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Update only provided fields
    for key, value in request.json.items():
        setattr(member, key, value)

    db.session.commit()
    return member_schema.jsonify(member)

# -----------------------
# DELETE MEMBER
# -----------------------
@members_bp.route('/', methods=['DELETE'])
@token_required
@limiter.limit("5 per day")
def delete_member(member_id):
    member = db.session.get(Member, member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted successfully"}), 200
