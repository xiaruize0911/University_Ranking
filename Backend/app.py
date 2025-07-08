from flask import Flask
from routes.universities import universities_bp
# from routes.rankings import rankings_bp
# from routes.stats import stats_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(universities_bp, url_prefix="/universities")
# app.register_blueprint(rankings_bp, url_prefix="/rankings")
# app.register_blueprint(stats_bp, url_prefix="/stats")

if __name__ == "__main__":
    app.run(debug=True)
