from app import application
import os

print ("app.pyBOL:")
print (__name__)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)

