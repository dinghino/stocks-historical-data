import os
from scraper import Settings
from cli import entry

# Settings object for the whole app

def start():
    settings = Settings()
    os.system('clear')
    
    if settings.init():
        print("Settings loaded")
        entry.run(settings)
    else:
        print("There was an error initializing the app")


if __name__ == "__main__":
    start()
