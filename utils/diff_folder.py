import os

def diff_folder (change_folder, snapshot_folder, task):

    if task == "postchange_snapshot_and_diff_prechange_snapshot":
        print("############################ compare postchange with prechange ############################")
        before_folder = os.path.join(change_folder, 'prechange_snapshot_0')
        os.system(f'pyats diff {before_folder} {snapshot_folder} --output {change_folder}/diff_dir')

    elif task == "postchange_snapshot_and_diff_last_postchange_snapshot":
        print("######################### compare postchange with last postchange ##########################")
        i = int(snapshot_folder.rsplit('_', 1)[-1]) -1
        before_folder = os.path.join(change_folder, ('postchange_snapshot_' + str(i)))
        os.system(f'pyats diff {before_folder} {snapshot_folder} --output {change_folder}/diff_dir')

    else:
        pass