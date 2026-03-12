from flask import Blueprint,make_response,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from constants import ALLOWED_ROLES
from tasks.email_tasks import send_role_change_email
from utils.role_required import role_required
from models.user import User
from extensions.db import db

admin_bp = Blueprint("admin",__name__)

@jwt_required()
@role_required(["admin"])
@admin_bp.route("/users")
def get_users():
    page = request.args.get("page",1,int)

    pagination = User.query.paginate(page=page,per_page=10,error_out=False)

    users = [{
        "username":user.username,
        "id":user.id,
        "email":user.email,
        "role":user.role
    } for user in pagination.items]

    return make_response({"users":users,"total":pagination.total,"current_page":pagination.page},200)

@admin_bp.route("/set_role/<username>", methods=["PATCH"])
@jwt_required()
@role_required(["admin"])
def set_role(username):

    data = request.json
    role = data.get("role")
    current_user_id = get_jwt_identity()

    if not role:
        return make_response({"message": "Role not present"}, 400)

    if role not in ALLOWED_ROLES:
        return make_response({"message": "Wrong role assigned"}, 400)

    user = User.query.filter_by(username=username).first()

    if not user:
        return make_response({"message": "User not found"}, 404)

    if user.id == current_user_id:
        return make_response({"message": "You cant change your own role"}, 400)

    if role == user.role:
        return make_response({"message": "No change in role"}, 400)

    if user.role == "admin":
        return make_response({"message": "Cant change role of an admin"}, 400)

    user.role = role

    send_role_change_email.delay(user.email, role)

    db.session.commit()

    return make_response({"message": f"User {username} role changed to {role}"})

@jwt_required()
@role_required(["admin"])
@admin_bp.route("/get_user/<username>")
def get_user(username):
    user = User.query.filter_by(username = username).first()

    if not user:
       return make_response({"message":"No such user exists"},404)
    
    res = {
        "username":user.username,
        "email":user.email,
        "role":user.role
    }

    return make_response({"user_data":res})

@jwt_required()
@role_required(["admin"])
@admin_bp.route("/get_user/<username>")
def get_specific_user(username):
    user = User.query.filter_by(username = username).first()

    if not user:
       return make_response({"message":"No such user exists"},404)
    
    res = {
        "username":user.username,
        "email":user.email,
        "role":user.role
    }

    return make_response({"user_data":res})

@jwt_required()
@role_required(["admin"])
@admin_bp.route("/delete_user/<username>",methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username = username).first()

    if not user:
       return make_response({"message":"No such user exists"},404)
    
    db.session.delete(user)
    db.session.commit()

    return make_response({"message":f"User {username} deleted"})
