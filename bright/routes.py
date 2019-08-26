from flask import request
import json

from .models import User


def configure_routes(app):
    @app.route('/', methods=['GET'])
    def get():
        return "Hello, world!", 200

    @app.route('/user', methods=['GET'])
    def user_get_all():
        app.logger.debug("Get all users")
        users = User.query.all()
        all_users = []
        for user in users:
            new_user = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "zip_code": user.zip_code,
                "email": user.email,
            }

            all_users.append(new_user)
        return json.dumps(all_users), 200

    @app.route('/user/<user_ids>', methods=['GET'])
    def user_get(user_ids):
        app.logger.debug(f"Get user or list of users, {user_ids}")
        ids = user_ids.split(',')
        users = User.query.filter(User.id.in_(ids)).all()
        all_users = []
        for user in users:
            new_user = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "zip_code": user.zip_code,
                "email": user.email,
            }
            all_users.append(new_user)
        return json.dumps(all_users), 200

    @app.route('/user/create', methods=['POST'])
    def user_create():
        app.logger.debug("Create user or list of users")
        data = request.get_json()
        if type(data) == dict:
            data = [data]

        for user in data:
            first_name = user['first_name'] if 'first_name' in user else ""
            last_name = user['last_name'] if 'last_name' in user else ""
            zip_code = user['zip_code'] if 'zip_code' in user else ""
            email = user["email"] if 'email' in user else ""

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                zip_code=zip_code,
                email=email
            )
            db.session.add(new_user)
        db.session.commit()
        return "Created", 200

    @app.route('/user/delete/<user_ids>', methods=['DELETE'])
    def user_delete(user_ids):
        app.logger.debug("Delete user or list of users")
        ids = user_ids.split(',')
        for i in ids:
            User.query.filter_by(id=i).delete()
        db.session.commit()
        return "Deleted", 200

    @app.route('/user/update', methods=['PATCH'])
    def user_update():
        app.logger.debug("Update user or list of users")
        data = request.get_json()
        if type(data) == dict:
            data = [data]
        for user in data:
            if 'id' in user:
                i = user['id']
                update_user = User.query.filter_by(id=i).first()
                if update_user is not None:
                    if 'first_name' in user:
                        update_user.first_name = user['first_name']
                    if 'last_name' in user:
                        update_user.last_name = user['last_name']
                    if 'zip_code' in user:
                        update_user.zip_code = user['zip_code']
                    if 'email' in user:
                        update_user.email = user["email"]
                    db.session.commit()

        return "Updated.", 200