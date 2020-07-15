
from classifier import app

if __name__ == '__main__':
    if 'serve' in sys.argv:
    uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
