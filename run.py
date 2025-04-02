from app import create_app
from app import db
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Usa a porta definida pelo Heroku
    app.run(host="0.0.0.0", port=port, debug=True)