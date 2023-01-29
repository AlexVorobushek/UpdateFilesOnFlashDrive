import json
import shutil
import hashlib
import os


def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


with open('sourse.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ORIGINAL_PATH, COPY_PATH = data["OriginalPath"], data["CopyPath"]


def del_item(path):
    if os.path.isdir(path):
        os.rmdir(path)
    else:
        os.remove(path)

def copy_item(org_path, cp_path, item):
    if os.path.isdir(org_path+item):
        shutil.copytree(org_path+item, cp_path+item)
    else:
        shutil.copy(org_path+item, cp_path)


def run(dop_path=''):
    Org_dir_set = set(os.listdir(ORIGINAL_PATH + dop_path))
    Cp_dir_set = set(os.listdir(COPY_PATH + dop_path)) - {"System Volume Information"}

    for item in Cp_dir_set - Org_dir_set: del_item(COPY_PATH + dop_path + item)
    for item in Org_dir_set - Cp_dir_set: copy_item(ORIGINAL_PATH + dop_path, COPY_PATH + dop_path, item)
    for item in Org_dir_set & Cp_dir_set:
        if os.path.isdir(ORIGINAL_PATH + dop_path + item): run(dop_path=f'{item}\\')
        elif get_hash_md5(ORIGINAL_PATH + dop_path + item) != get_hash_md5(COPY_PATH + dop_path + item):
            shutil.copyfile(ORIGINAL_PATH + dop_path + item, COPY_PATH + dop_path + item)
run()