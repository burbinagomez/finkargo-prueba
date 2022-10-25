from crypt import methods
from urllib import response
from flask import Flask, request, make_response, current_app
from middleware import token_required,save_general_data
from werkzeug.security import generate_password_hash,check_password_hash
from models import db
import models
import os
import jwt
import datetime
import uuid
from peewee import *

models.create_tables()

app = Flask(__name__)
app.config['SECRET_KEY']= os.getenv("SECRET_KEY")

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.route("/user/create", methods=['POST'])
def create_user():
    r = request.get_json()
    response = None
    try:
        user = {
            "name" : r.get("name"),
            "email" : r['email'],
            "password" : generate_password_hash(r['password'], method='sha256'),
            "country": r['country'],
            "role": r['role'],
            "company": r['company']
        }
        if models.User().create(**user):
            response = make_response("Transaccion Correcta",200)
        else:
            response = make_response("Transaccion Incorrecta", 500)
    except Exception as e:
        response = make_response(str(e),500)
    finally:
        return response 

@app.route("/user/login", methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password: 
        return make_response('could not verify', 401, {'Authentication': 'login required"'})   
    
    user = models.User.get(models.User.email == auth.username)
    if check_password_hash(user.password, auth.password):
        payload = {
                'id' : str(user.id),
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
            }
        print(payload)
        token = jwt.encode(
            payload, 
            app.config['SECRET_KEY'], 
            algorithm="HS256"
            )
    
        return make_response({'token' : token},200)
    
    return make_response('could not verify',  401, {'Authentication': '"login required"'})

@app.route("/company/create", methods=['POST'])
@token_required
def create_company(current_user):
    r = request.get_json()
    response = None
    try:
        company = {
            "name": r['name']
        }
        if models.Company.create(**company):
            response = make_response("Transaccion Correcta", 200)
        else:
            response = make_response("Transaccion Incorrecta", 500)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

@app.route("/company/update", methods=['PUT'])
@token_required
def update_company(current_user):
    r = request.get_json()
    response = None
    try:
        company = models.Company.get_by_id(r['id'])
        company.name = r['name']
        company.save()
        if company.save():
            response = make_response("Transaccion Correcta", 200)
        else:
            response = make_response("Transaccion Incorrecta", 500)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

@app.route("/company/delete", methods=['DELETE'])
@token_required
def delete_company(current_user):
    response = None
    try:
        id = request.args.get('id')
        company = models.Company.get_by_id(id)
        if company:
            company.delete_instance()
            response = make_response("Transaccion correcta" , 200)
        else:
            response = make_response(f"Id: {id} not found", 404)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

@app.route("/company/get", methods=['GET'])
@token_required
def get_company(current_user):
    response = None
    try:
        id = request.args.get('id')
        company = models.Company.get_by_id(id)
        if company:
            response = make_response(company.select().dicts()[0] , 200)
        else:
            response = make_response(f"Id: {id} not found", 404)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

@app.route("/company/get/all", methods=['GET'])
@token_required
def get_companies(current_user):
    response = None
    try:
        companies = [company for company in models.Company.select().dicts()]
        response = make_response(companies, 200)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

# Role
@app.route("/role/create", methods=['POST'])
@token_required
def create_role():
    r = request.get_json()
    response = None
    try:
        role = {
            "name": r['name']
        }
        if models.Role.create(**role):
            response = make_response("Transaccion Correcta", 200)
        else:
            response = make_response("Transaccion Incorrecta", 500)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

@app.route("/role/update", methods=['PUT'])
@token_required
def update_role():
    r = request.get_json()
    response = None
    try:
        role = models.Role.get_by_id(r['id'])
        role.name = r['name']
        role.save()
        if role.save():
            response = make_response("Transaccion Correcta", 200)
        else:
            response = make_response("Transaccion Incorrecta", 500)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

@app.route("/role/delete", methods=['DELETE'])
@token_required
def delete_role():
    response = None
    try:
        id = request.args.get('id')
        role = models.Role.get_by_id(id)
        if role:
            role.delete_instance()
            response = make_response("Transaccion correcta" , 200)
        else:
            response = make_response(f"Id: {id} not found", 404)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

@app.route("/role/get", methods=['GET'])
@token_required
def get_role():
    response = None
    try:
        id = request.args.get('id')
        role = models.Role.get_by_id(id)
        if role:
            response = make_response(role.select().dicts()[0] , 200)
        else:
            response = make_response(f"Id: {id} not found", 404)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

@app.route("/role/get/all", methods=['GET'])
@token_required
def get_roles():
    response = None
    try:
        roles = [role for role in models.Role.select().dicts()]
        response = make_response(roles, 200)
    except Exception as e:
        response = make_response(str(e), 500)
    finally:
        return response

#Form
@app.route("/form/submit", methods=["POST"])
@save_general_data
def submit_form():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    try:
        if not token:
            r = request.get_json()
            user = models.User.create(**{
                "name": f'Anonimo {uuid.uuid4()}',
                "country": models.Country.get_by_id(r['country']),
                "company": models.Company.get_by_id(r['company']),
                "role": models.Role.get_by_id(r['role']),
            })

            form = models.Form.create(**{
                "user": user,
                "answer":r['answer']  
            })

            if form:
                return make_response("Transaccion correcta",200)
            else:
                return make_response("Transaccion Incorrecta",500)
        else:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user = models.User.get_by_id(data['id'])
            if user is None:
                return make_response({
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401)
            r = request.get_json()
            form = models.Form.create(**{
                "user": user,
                "answer":r['answer']  
            })
            if form:
                return make_response("Transaccion correcta",200)
            else:
                return make_response("Transaccion Incorrecta",500)
    except Exception as e:
        return make_response(str(e),500)

#Reports
@app.route("/reports/country", methods=["GET"])
def reports_country():
    try:
        q = models.Form.select(
            models.Country.name, 
            fn.COUNT(models.Form.id).alias('conteo')
            ).where(models.Form.answer <= 6).join(models.User).join(models.Country).group_by(models.Country.name).order_by(+models.Form.answer)
        forms = [form for form in q.dicts()[:3]]
        return make_response(forms,200)
    except Exception as e:
        return make_response(str(e),500)

@app.route("/reports/role", methods=["GET"])
def reports_role():
    try:
        q = models.Form.select(
            models.Role.name, 
            fn.COUNT(models.Form.id).alias('conteo')
            ).where(models.Form.answer >= 9, models.Form.answer <= 10 ).join(models.User).join(models.Role).group_by(models.Role.name).order_by(+models.Form.answer)
        forms = [form for form in q.dicts()[:3]]
        return make_response(forms,200)
    except Exception as e:
        return make_response(str(e),500)
