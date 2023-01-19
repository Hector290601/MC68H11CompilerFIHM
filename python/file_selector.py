import easygui

def select_file():
    path = easygui.fileopenbox()
    return path

if __name__ == "__main__":
    print(select_file())
