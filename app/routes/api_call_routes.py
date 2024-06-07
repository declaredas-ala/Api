from flask import Blueprint, request, jsonify
from app.controller.api_call_controller import (
    log_api_call,
    get_api_calls_by_filters,
    get_api_call_by_id,
    update_api_call,
    delete_api_call,
    retry_api_call,
    get_all_api_calls,
)
from flask_jwt_extended import jwt_required

api_call_bp = Blueprint("api_call_bp", __name__)


@api_call_bp.route("/api-calls/", methods=["POST"])
def log_api_call_route():
    data = request.get_json()
    log_api_call(
        user_id=data["user_id"],
        api_endpoint=data["api_endpoint"],
        success=data["success"],
        response_code=data["response_code"],
    )
    return jsonify({"message": "API call logged successfully"}), 201


@api_call_bp.route("/api-calls/", methods=["GET"])
def get_api_calls_route():
    filters = request.args.to_dict()
    api_calls = get_api_calls_by_filters(filters)
    return jsonify(
        [
            {
                "id": call.id,
                "user_id": call.user_id,
                "api_endpoint": call.api_endpoint,
                "call_time": call.call_time,
                "success": call.success,
                "response_code": call.response_code,
            }
            for call in api_calls
        ]
    ), 200


@api_call_bp.route("/api-calls/<int:api_call_id>", methods=["GET"])
def get_api_call_by_id_route(api_call_id):
    api_call = get_api_call_by_id(api_call_id)
    if not api_call:
        return jsonify({"error": "API call not found"}), 404
    return jsonify(
        {
            "id": api_call.id,
            "user_id": api_call.user_id,
            "api_endpoint": api_call.api_endpoint,
            "call_time": api_call.call_time,
            "success": api_call.success,
            "response_code": api_call.response_code,
        }
    ), 200


@api_call_bp.route("/api-calls/<int:api_call_id>", methods=["PUT"])
def update_api_call_route(api_call_id):
    data = request.get_json()
    updated = update_api_call(api_call_id, data)
    if not updated:
        return jsonify({"error": "Failed to update API call"}), 500
    return jsonify({"message": "API call updated successfully"}), 200


@api_call_bp.route("/api-calls/<int:api_call_id>", methods=["DELETE"])
def delete_api_call_route(api_call_id):
    deleted = delete_api_call(api_call_id)
    if not deleted:
        return jsonify({"error": "Failed to delete API call"}), 500
    return jsonify({"message": "API call deleted successfully"}), 200


@api_call_bp.route("/api-calls/retry/<int:api_call_id>", methods=["POST"])
def retry_api_call_route(api_call_id):
    retry_api_call(api_call_id)
    return jsonify({"message": "API call retried successfully"}), 200


@api_call_bp.route("/api-calls/all", methods=["GET"])
def get_all_api_calls_route():
    api_calls = get_all_api_calls()
    return jsonify(
        [
            {
                "id": call.id,
                "user_id": call.user_id,
                "api_endpoint": call.api_endpoint,
                "call_time": call.call_time,
                "success": call.success,
                "response_code": call.response_code,
            }
            for call in api_calls
        ]
    ), 200
