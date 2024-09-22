from flask import Flask

from blueprints.calculator import calculator_bp
from blueprints.index import index_bp
from blueprints.post import post_bp
from blueprints.shorts import shorts_bp
from blueprints.thinking import thinking_bp
from blueprints.post_detail import post_detail_bp
from blueprints.top_nav import top_nav_bp

app = Flask(__name__)
app.register_blueprint(index_bp)
app.register_blueprint(post_bp)
app.register_blueprint(shorts_bp)
app.register_blueprint(thinking_bp)
app.register_blueprint(calculator_bp)
app.register_blueprint(post_detail_bp)
app.register_blueprint(top_nav_bp)

if __name__ == '__main__':
    app.run(debug=True)
