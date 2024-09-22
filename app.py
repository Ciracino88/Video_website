from flask import Flask
from dotenv import load_dotenv
import os

from blueprints.calculator import calculator_bp
from blueprints.index import index_bp
from blueprints.post import post_bp
from blueprints.shorts import shorts_bp
from blueprints.thinking import thinking_bp
from blueprints.post_detail import post_detail_bp
from blueprints.top_nav import top_nav_bp
from blueprints.login import login_bp

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SESSION_SECRET_KEY')
app.register_blueprint(index_bp)
app.register_blueprint(post_bp)
app.register_blueprint(shorts_bp)
app.register_blueprint(thinking_bp)
app.register_blueprint(calculator_bp)
app.register_blueprint(post_detail_bp)
app.register_blueprint(top_nav_bp)
app.register_blueprint(login_bp)
if __name__ == '__main__':
    app.run(debug=True)
