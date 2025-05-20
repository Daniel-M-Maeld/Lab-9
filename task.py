from flask import Flask, request, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///days.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


# Создание базы данных
with app.app_context():
    db.create_all()


@app.route('/')
def Sum():
    return render_template('Sum.html')

@app.route('/Day')
def Day():
    return render_template('Day.html')

@app.route("/api/users/sum", methods=["GET"])
def get_steps_sum():
    total = db.session.query(db.func.sum(User.name)).scalar() or 0
    return jsonify({"total_steps": total})

# Получение всех пользователей
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


# Добавление пользователя
@app.route("/api/users", methods=["POST"])
def add_user():
    data = request.get_json()
    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


# Удаление пользователя
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)