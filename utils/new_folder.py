import os

def create_folder(folder_name=None):
    path = folder_name
    if not os.path.exists(path):
        print("#"*5 + f' create new folder {path} ' + "#"*5)
        os.makedirs(path)
    path = os.path.join(os.getcwd(), path)  
    return path    