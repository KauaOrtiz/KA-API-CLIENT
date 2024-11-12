from flask import Flask, jsonify, request, session, redirect, url_for
from datetime import datetime, date
from bd import (
    createEnterprise, 
    getEnterprise, 
    createEmployee, 
    getEmployee,
    checkFinalPoint,
    startPoint,
    getAllPoints,
    finalPoint,
    getDayPoint,
    deletePoint,
    editPoint
)

app = Flask(__name__)
app.secret_key = 'chave_secreta'


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the API"})


@app.route("/login/employee", methods=['POST'])
def loginEmployee():
    data = request.json
    if 'username' in data:
        username = data['username']
        password = data['password']
        result = getEmployee(username, password)
        data = result.json

        if username == 'admin' and password == 'password':
            return jsonify({"message": "Admin login successful"}), 200
        
        elif data['message'] == "success":
            session['id_user'] = data['id_user']
            return jsonify({"message": "Employee login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
            
    elif 'new_username' in data:
        new_username = data['new_username']
        enterprise = data['enterprise']
        position = data['position']
        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password == confirm_password:
            result = createEmployee(new_username, enterprise, position, new_password)
            data = result.json

            if data['message'] == "success":
                return jsonify({"message": "User created successfully"}), 201
            else:
                return jsonify({"error": data["message"]}), 400
        else:
            return jsonify({"error": "Passwords don't match"}), 400


@app.route("/login/enterprise", methods=['POST'])
def loginEnterprise():
    data = request.json
    if 'company' in data:
        company = data['company']
        password = data['password']
        result = getEnterprise(company, password)
        data = result.json

        if company == 'admin' and password == 'password':
            return jsonify({"message": "Admin login successful"}), 200
        
        elif data['message'] == "success":
            session['id_empresa'] = data['id_empresa']
            return jsonify({"message": "Enterprise login successful"}), 200
        else:
            return jsonify({"error": data["message"]}), 401
            
    elif 'new_company' in data:
        new_company = data['new_company']
        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password == confirm_password:
            result = createEnterprise(new_company, new_password)
            data = result.json
            return jsonify({"message": data["message"]}), 201
        else:
            return jsonify({"error": "Passwords don't match"}), 400


@app.route("/dashboard/employee", methods=['POST'])
def dashboardEmployee():
    user_id = session.get('id_user')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 403

    result2 = checkFinalPoint(user_id, date.today())
    data2 = result2.json

    if data2["message"] == "success":
        ponto = getDayPoint(user_id, date.today())
        dados = ponto.json
        result4 = finalPoint(dados['id_ponto'], getDatetime())
        data4 = result4.json
        if data4['message'] == "success":
            return jsonify({"message": "Exit point recorded"}), 200
    else:
        result = startPoint(user_id, getDatetime())
        return jsonify({"message": "Entry point recorded"}), 200


@app.route("/dashboard/enterprise", methods=['GET', 'PUT', 'DELETE'])
def dashboardEnterprise():
    company_id = session.get('id_empresa')
    if not company_id:
        return jsonify({"error": "Enterprise not logged in"}), 403

    if request.method == "GET":
        result = getAllPoints(company_id)
        pontos = result.json
        return jsonify({"points": pontos}), 200

    elif request.method == "PUT":
        data = request.json
        id_ponto = data["id_ponto"]
        hora_inicio = datetime.strptime(data["hora_inicio"], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S.%f')
        hora_final = datetime.strptime(data["hora_final"], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S.%f')

        result = editPoint(id_ponto, hora_inicio, hora_final)
        data = result.json
        if data['message'] == 'success':
            return jsonify({"message": "Point updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update point"}), 400

    elif request.method == "DELETE":
        id_ponto = request.json["id_ponto"]
        result = deletePoint(id_ponto)
        data = result.json
        if data['message'] == 'success':
            return jsonify({"message": "Point deleted successfully"}), 200
        else:
            return jsonify({"error": "Point not found"}), 404


def getDatetime():
    agora = datetime.now()
    return agora


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
