import os


while True:
    os.system("python TaggedBot.py")
    os.system("heroku dyno:restart --app tagged-bot-2-usa")
    os.system("python restart.py")

