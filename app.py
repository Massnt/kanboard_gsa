import os
from kanboard_gsa_api import criar_app
from dotenv import load_dotenv

app = criar_app()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('APP_PORT'))
