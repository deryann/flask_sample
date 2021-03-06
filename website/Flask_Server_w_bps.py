from flask import Flask
import os
from blueprints.RestAPIGroupA import api_group_a

app = Flask(__name__)

app.register_blueprint(api_group_a, url_prefix='/api_group_a')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
