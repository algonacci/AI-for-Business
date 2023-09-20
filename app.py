from flask import Flask

from index import bp as index_bp
from customer_segmentation import bp as customer_bp

app = Flask(__name__)

app.register_blueprint(index_bp)
app.register_blueprint(customer_bp)

if __name__ == "__main__":
    app.run()
