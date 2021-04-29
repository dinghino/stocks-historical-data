import os
from scraper import Settings
from cli import entry

# Settings object for the whole app

def start():
    settings = Settings()
    os.system('clear')
    
    if settings.init():
        print("Settings loaded")
    else:
        print("There was an error Loading the settings")

    entry.run(settings)

if __name__ == "__main__":
    start()
