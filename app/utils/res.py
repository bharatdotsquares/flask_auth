from flask import jsonify
def res(success=True, message=None, data=None, status_code=200):
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    }), status_code
