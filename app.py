from app import application
import os

if __name__ == "__main__":
    print(os.getcwd())
    # Creating the directories for the deployed app -- should also delete these dirs sometimes
    os.mkdir('../Flasklast/app/static/client')
    os.mkdir('../Flasklast/app/static/client/audiofiles')
    os.mkdir('../Flasklast/app/static/client/images')
    os.mkdir('../Flasklast/app/static/client/IncomingAudio')

    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)

