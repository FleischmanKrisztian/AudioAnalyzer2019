from app import application

print ("app.pyBOL:")
print (__name__)
if __name__ == "app":
    application.run(debug=False)
