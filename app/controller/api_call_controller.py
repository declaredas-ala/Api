from app.model import db
from app.model.models import ApiCall


def log_api_call(user_id, api_endpoint, success, response_code):
    api_call = ApiCall(
        user_id=user_id,
        api_endpoint=api_endpoint,
        success=success,
        response_code=response_code,
    )
    db.session.add(api_call)
    db.session.commit()


def get_all_api_calls():
    return db.session.query(ApiCall).all()


def get_api_calls_by_filters(filters):
    query = db.session.query(ApiCall)
    if "user_id" in filters:
        query = query.filter(ApiCall.user_id == filters["user_id"])
    if "success" in filters:
        query = query.filter(ApiCall.success == filters["success"])
    if "api_endpoint" in filters:
        query = query.filter(ApiCall.api_endpoint == filters["api_endpoint"])
    if "start_date" in filters and "end_date" in filters:
        query = query.filter(
            ApiCall.call_time.between(filters["start_date"], filters["end_date"])
        )
    return query.all()


def get_api_call_by_id(api_call_id):
    return db.session.query(ApiCall).get(api_call_id)


def update_api_call(api_call_id, data):
    api_call = db.session.query(ApiCall).get(api_call_id)
    if not api_call:
        return False
    for key, value in data.items():
        setattr(api_call, key, value)
    db.session.commit()
    return True


def delete_api_call(api_call_id):
    api_call = db.session.query(ApiCall).get(api_call_id)
    if not api_call:
        return False
    db.session.delete(api_call)
    db.session.commit()
    return True


def retry_api_call(api_call_id):
    api_call = db.session.query(ApiCall).get(api_call_id)
    if api_call:
        # Logic to retry the API call
        pass
