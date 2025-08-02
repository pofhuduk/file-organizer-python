import os
import dotenv
import json
import shutil

def load_config(config_file:str):
    with open(config_file, 'r') as f:
        return json.load(f)
    
def check_file(file_name:str, config:dict):
    file_name = file_name.lower()
    key_list = config['special_files'].keys()
    for i in key_list:
        if file_name.endswith(i):
            return config['special_files'][i]
    
    file_extension = os.path.splitext(file_name)[-1]
    folders = config['folders']
    for i in folders:
        if (file_extension in folders[i]):
            return i
    return 'Other'    

def move_file(directory:str, file_name:str, folder_name:str):
    path = os.path.join(directory, file_name) 
    
    if os.path.isdir(path):
        return None

    new_directory = os.path.join(directory, folder_name)
    new_path = os.path.join(new_directory, file_name)
    
    shutil.move(path, new_path)

dotenv.load_dotenv()
DIR = os.getenv('DIR')

if not DIR:
    print("Error: The 'DIR' environment variable is not set or"
    "is empty. Please define it in your .env file.")
    exit()

if not os.path.isdir(DIR):
    print(f"Error: The path '{DIR}' does not exist or is not a directory.")
    exit()

config = load_config(config_file='config.json') #add error check for json

file_list = os.listdir(DIR)
for i in file_list:
    folder_name = check_file(file_name=i, config=config)
    folder_path = os.path.join(DIR,folder_name)
    os.makedirs(folder_path, exist_ok=True)

    move_file(directory=DIR, folder_name=folder_name, file_name=i)
