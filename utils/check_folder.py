import os
from utils.new_folder import create_folder

def check_folder(change_folder, test_type):
    snapshot_folder = ""
    
    if test_type.startswith('prechange_snapshot'):
        for i in range(20):
            snapshot_folder = os.path.join(change_folder, ('prechange_snapshot_' + str(i)))
            if not os.path.exists(snapshot_folder):
                create_folder(snapshot_folder)
                break
    elif test_type.startswith('postchange_snapshot'):
        for i in range(20):
            snapshot_folder = os.path.join(change_folder, ('postchange_snapshot_' + str(i)))
            if not os.path.exists(snapshot_folder):
                create_folder(snapshot_folder)
                break
    else:
        print("test type not supported")

    return snapshot_folder    