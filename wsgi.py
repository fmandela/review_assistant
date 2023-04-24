import os
from dotenv import load_dotenv 

from src.main import app

# load_dotenv()

PORT =  os.getenv('PORT', 8080)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
