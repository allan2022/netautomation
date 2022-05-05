import os

def create_folder(folder_name=None):
    path = folder_name
    if not os.path.exists(path):
        print("\n" + "#"*15 + f' create new folder {path} ' + "#"*15)
        os.makedirs(path)
    path = os.path.join(os.getcwd(), path)  
    return path    