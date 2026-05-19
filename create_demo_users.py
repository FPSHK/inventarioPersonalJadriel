from app import create_app, db
from app.models import Role, User
from werkzeug.security import generate_password_hash


app = create_app()

with app.app_context():
    # Asegurarse de la existencia de los roles
    roles = ['Admin', 'Usuario', 'Owner']
    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            print(f' Rol"{role_name}" creado.')

    db.session.commit()

    #Diccionario con usuarios a insertar
    users_data = [
        {
            "username": "Administrator",
            "email": "admin@example.com",
            "password": "admin1234",
            "role_name": "Admin",
        },
        {
            "username": "Item Owner",
            "email": "owner@example.com",
            "password": "owner123",
            "role_name": "Owner"
        },
        {
            "username": "Regular User",
            "email": "user@example.com",
            "password": "user12",
            "role_name": "Usuario"
        }
    ]

    for user_info in users_data:
        existing_user = User.query.filter_by(email=user_info['email']).first()
        if not existing_user:
            role = Role.query.filter_by(name=user_info['role_name']).first()
            user = User(
                username=user_info['username'],
                email=user_info['email'],
                role = role
            )
            user.set_password(user_info['password']) #generar hash seguro
            db.session.add(user)
            print(f' Usuario "{user.username}" creado con rol "{role.name}".')
        else:
            print(f' El usuario con email {user_info["email"]} ya existe.')

    db.session.commit()
    print(" Todos los usuarios fueron procesados correctamente.")