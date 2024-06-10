from flask import Blueprint, request, Response
from app.controller.api_call_controller import (
    add_api_call,
    get_all_api_calls,
    get_api_call_by_id,
    update_api_call,
    delete_api_call,
    launch_api_call,
)

api_call_bp = Blueprint("api_call_bp", __name__)


# Route to add a new API call
@api_call_bp.route("/api-calls/", methods=["POST"])
def add_new_api_call():
    data = request.get_json()
    user_id = data.get("user_id")
    api_endpoint = data.get("api_endpoint")
    type = data.get("type")
    request_body = data.get("request_body")
    return add_api_call(user_id, api_endpoint, type, request_body)


# Route to retrieve all API calls
@api_call_bp.route("/api-calls/", methods=["GET"])
def get_all_api_calls_route():
    return get_all_api_calls()


# Route to retrieve an API call by ID
@api_call_bp.route("/api-calls/<int:api_call_id>", methods=["GET"])
def get_api_call_by_id_route(api_call_id):
    return get_api_call_by_id(api_call_id)


# Route to update an API call by ID
@api_call_bp.route("/api-calls/<int:api_call_id>", methods=["PUT"])
def update_api_call_route(api_call_id):
    return update_api_call(api_call_id)


# Route to delete an API call by ID
@api_call_bp.route("/api-calls/<int:api_call_id>", methods=["DELETE"])
def delete_api_call_route(api_call_id):
    return delete_api_call(api_call_id)


@api_call_bp.route("/ala", methods=["GET"])
def ala():
    return Response("hello", status=200)


# Route to launch an API call
@api_call_bp.route("/api-calls/launch/<int:api_call_id>", methods=["POST"])
def launch_api_call_route(api_call_id):
    return launch_api_call(api_call_id)
