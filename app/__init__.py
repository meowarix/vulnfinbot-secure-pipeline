from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import bp
    app.register_blueprint(bp)

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        return response

    return app
