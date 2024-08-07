from flask import Flask

def registrar_rotas(app : Flask):
    from .kanboard_hook import bp as kanboard_hook_bp
    app.register_blueprint(kanboard_hook_bp)