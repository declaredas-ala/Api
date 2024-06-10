from flask import jsonify, request
from app.model import db
from app.model.models import ApiCall
import requests  # For making external API calls


# Function to add an API call
def add_api_call(user_id, api_endpoint, type, request_body):
    try:
        api_call = ApiCall(
            user_id=user_id,
            api_endpoint=api_endpoint,
            type=type,
        )
        db.session.add(api_call)
        db.session.commit()
        return jsonify({"message": "API call added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Function to retrieve all API calls
def get_all_api_calls():
    try:
        api_calls = db.session.query(ApiCall).all()
        api_calls_data = [
            {
                "id": api_call.id,
                "user_id": api_call.user_id,
                "api_endpoint": api_call.api_endpoint,
                "type": api_call.type,
                "response_code": api_call.response_code,
                "response": api_call.response,
            }
            for api_call in api_calls
        ]
        return jsonify(api_calls_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Function to retrieve an API call by ID
def get_api_call_by_id(api_call_id):
    try:
        api_call = db.session.query(ApiCall).get(api_call_id)
        if not api_call:
            return jsonify({"error": "API call not found"}), 404
        api_call_data = {
            "id": api_call.id,
            "user_id": api_call.user_id,
            "api_endpoint": api_call.api_endpoint,
            "type": api_call.type,
            "response_code": api_call.response_code,
            "response": api_call.response,
        }
        return jsonify(api_call_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Function to update an API call
def update_api_call(api_call_id):
    try:
        data = request.get_json()
        api_call = db.session.query(ApiCall).get(api_call_id)
        if not api_call:
            return jsonify({"error": "API call not found"}), 404
        api_call.type = data.get("type", api_call.type)
        api_call.response_code = data.get(
            "status", api_call.response_code
        )  # Ensure 'status' is used as key for response_code
        api_call.api_endpoint = data.get("api_endpoint", api_call.api_endpoint)
        api_call.response = data.get("response", api_call.response)
        api_call.response_code = data.get("response_code", api_call.response_code)
        db.session.commit()
        return jsonify({"message": "API call updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Function to delete an API call
def delete_api_call(api_call_id):
    try:
        api_call = db.session.query(ApiCall).get(api_call_id)
        if not api_call:
            return jsonify({"error": "API call not found"}), 404
        db.session.delete(api_call)
        db.session.commit()
        return jsonify({"message": "API call deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Function to launch an API call and update the response and status code
def launch_api_call(api_call_id):
    try:
        api_call = db.session.query(ApiCall).get(api_call_id)
        if not api_call:
            return jsonify({"error": "API call not found"}), 404

        if api_call.type == "GET":
            response = requests.get(api_call.api_endpoint)
        elif api_call.type == "POST":
            response = requests.post(api_call.api_endpoint, data=api_call.request_body)
        elif api_call.type == "PUT":
            response = requests.put(api_call.api_endpoint, data=api_call.request_body)
        elif api_call.type == "DELETE":
            response = requests.delete(api_call.api_endpoint)
        else:
            return jsonify({"error": "Invalid request type"}), 400

        api_call.response_code = response.status_code
        api_call.response = response.text
        db.session.commit()

        return jsonify(
            {
                "message": "API call executed successfully",
                "response": api_call.response,
                "response_code": api_call.response_code,
            }
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
