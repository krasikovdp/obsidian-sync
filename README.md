# Obsidian Sync
Sync script for obsidian because I don't wanna pay 4 bucks a month.

## Usage and quirks
Run the script before and after editing a vault. It does not support vault deletion. You can delete a vault through Obsidian but the script will sync it anyway. If you wanna avoid that, edit the [Pantry](https://getpantry.cloud/#) manually. If you have both local and remote changes, it will overwrite the remote vault. If the only changes you make are creating folders and/or moving files between them, then it should not sync. If you just rename files, it may or may not sync. It syncs only if a file is created, changed or deleted.

## Storage
Script uses [Pantry](https://getpantry.cloud/#) for storage. It's easy to set up and gives 100MB of storage for free. You need to create a pantry and then create a basket in it. You will need to use the pantry's id and the basket's name in settings.py

## Settings
You will need to create a file settings.py inside the project folder with the following variables:
```
VAULTS_DIR = ''  # path to the directory that contains your vaults
PANTRY_ID = ''  # the id of your pantry
BASKET_NAME = ''  # the name of a basket in your pantry
```

## Android
Supports usage through termux. You will need to install [Termux](https://f-droid.org/en/packages/com.termux/) and [Termux:Widget](https://f-droid.org/en/packages/com.termux.widget/) from [F-Droid](https://f-droid.org/en/) (the google play version is outdated and probably won't work) then run the following commands:
```
apt update
apt upgrade
pkg install git
pkg install python
pip install requests
git clone https://github.com/krasikovdp/obsidian-sync.git
mkdir .shortcuts
touch .shortcuts/obsidian-sync.sh
chmod +x .shortcuts/obsidian-sync.sh
echo "python ~/obsidian-sync/obsidian_sync.py" > .shortcuts/obsidian-sync.sh
touch obsidian-sync/settings.py
```
and allow storage access, then edit the settings.py file with vim, for example. Finding the vaults' directory can be tricky. 
/data/data/com.termux/files/home/storage/shared/Obsidian works for me, where Obsidian is at the root of my storage. You can transfer the pantry id to your phone with [protectedtext](https://www.protectedtext.com/).
Now you can create a widget on your desktop that will run the script.
If you have an IPhone, I feel sorry for you.
