from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

users = {
    "user001": {
        "medications": [
            {"name": "Aspirin", "time": "08:00", "taken": False},
            {"name": "Metformin", "time": "12:00", "taken": False}
        ],
        "history": []
    }
}

@app.route('/medications/<user_id>', methods=['GET'])
def get_medications(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user['medications'])

@app.route('/medications/<user_id>/mark', methods=['POST'])
def mark_medication(user_id):
    data = request.json
    med_name = data.get("name")
    user = users.get(user_id)

    for med in user['medications']:
        if med["name"] == med_name:
            med["taken"] = True
            user["history"].append({
                "name": med_name,
                "taken_at": datetime.now().isoformat()
            })
            return jsonify({"message": f"{med_name} marked as taken."})

    return jsonify({"error": "Medication not found"}), 404

@app.route('/education/<user_id>', methods=['GET'])
def get_education(user_id):
    return jsonify({
        "tips": [
            "식후 30분 이내 복용하세요.",
            "복약 전에는 충분히 물을 섭취하세요.",
            "어지럼증이 심할 경우 복용을 중단하고 의사에게 연락하세요."
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
