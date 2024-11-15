from pathlib import Path
from base64 import b64decode, b64encode
import requests
import json
import hashlib
import shutil
import time
import subprocess
from settings import *


class PantryBasket:
    def __init__(self, pantry_id, basket_name):
        self.pantry_id = pantry_id
        self.basket_name = basket_name


    def get(self):
        return requests.get(f'https://getpantry.cloud/apiv1/pantry/{self.pantry_id}/basket/{self.basket_name}').json()

    def set(self, data):
        resp = requests.put(f'https://getpantry.cloud/apiv1/pantry/{self.pantry_id}/basket/{self.basket_name}', json=data)
        assert  resp.status_code == 200
        return resp.json()


def main():
    basket = PantryBasket(PANTRY_ID, BASKET_NAME)
    data = basket.get()
    vaults_path = Path(VAULTS_DIR)
    sync_info_file = vaults_path.joinpath('sync_info.json')
    if not sync_info_file.exists():
        sync_info = {}
    else:
        sync_info = json.loads(sync_info_file.read_text())
    zip_files = []
    local_vaults = []
    for path in vaults_path.iterdir():
        if path.is_dir():
            name = path.stem
            local_vaults.append(name)
            sync_info.setdefault(name, {})
            sync_info[name].setdefault('last_edit', 0)
            sync_info[name].setdefault('md5', '')

            zip_files.append(vaults_path.joinpath(name + '.zip'))
            shutil.make_archive(vaults_path.joinpath(name), 'zip', path)
            hash = hashlib.md5(zip_files[-1].read_bytes()).digest().hex()
            sync_info[name]['md5'] = hash
            cur_time = int(time.time())
            data['vaults'].setdefault(name, {'md5': '-', 'last_edit': -1})
            if hash != data['vaults'][name]['md5']:
                sync_info[name]['last_edit'] = cur_time
                if data['vaults'][name]['last_edit'] < sync_info[name]['last_edit']:
                    data['vaults'][name]['file'] = b64encode(zip_files[-1].read_bytes()).decode('utf-8')
                    data['vaults'][name]['md5'] = sync_info[name]['md5']
                    data['vaults'][name]['last_edit'] = sync_info[name]['last_edit']
                else:
                    zip_files[-1].write_bytes(b64decode(data['vaults'][name]['file']))
                    sync_info[name]['md5'] = data['vaults'][name]['md5']
                    sync_info[name]['last_edit'] = data['vaults'][name]['last_edit']
    for name in data['vaults'].keys():
        if name not in local_vaults:
            zip_files.append(vaults_path.joinpath(name + '.zip'))
            zip_files[-1].touch()
            zip_files[-1].write_bytes(b64decode(data['vaults'][name]['file']))
            sync_info[name] = {}
            sync_info[name]['md5'] = data['vaults'][name]['md5']
            sync_info[name]['last_edit'] = data['vaults'][name]['last_edit']
    for zip_file in zip_files:
        vault = vaults_path.joinpath(zip_file.stem)
        try:
            shutil.rmtree(vault)
        except FileNotFoundError:
            pass  # if new vault is fetched
        vault.mkdir()
        shutil.unpack_archive(zip_file, vault, 'zip')
        zip_file.unlink()
    sync_info_file.write_text(json.dumps(sync_info, indent=2))
    basket.set(data)


def test():
    pass


if __name__ == '__main__':
    try:
        main()
        try:
            subprocess.call(['termux-toast', 'Success'])
        except FileNotFoundError:
            pass
    except Exception as e:
        with open('exception.txt', 'w') as file:
            file.write(str(e))
        try:
            subprocess.call(['termux-toast', 'Failed'])
        except FileNotFoundError:
            pass
