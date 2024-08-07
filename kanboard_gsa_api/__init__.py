from flask import Flask

def criar_app():
    app = Flask(__name__)

    with app.app_context():
        from .routes import registrar_rotas
        registrar_rotas(app)

    return app
