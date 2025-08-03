import os
import dotenv
import json
import shutil

def load_config(config_file:str):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Error: Configuration file {config_file} not found.')
        return None
    except json.JSONDecodeError:
        print(f'Error: Configuration file {config_file} is not valid JSON format.')
        return None

def load_env_vars():
    dotenv.load_dotenv()
    DIR = os.getenv('DIR')
    
    if not DIR:
        print("Error: The 'DIR' environment variable is not set or"
        "is empty. Please define it in your .env file.")
        exit()
    if not os.path.isdir(DIR):
        print(f"Error: The path '{DIR}' does not exist or is not a directory.")
        exit()
    
    return DIR

def check_file(file_name:str, config:dict, directory:str):
    full_path = os.path.join(directory, file_name)
    if os.path.isdir(full_path):
        if file_name in config['main_folders']:
            return None
        return 'Folders'

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
    
    new_directory = os.path.join(directory, folder_name)
    new_path = os.path.join(new_directory, file_name)
    
    try:
        shutil.move(path, new_path)
    except FileExistsError:
        print('Skipping: There is already a file with'
              f'{file_name} name on {folder_name} folder.')
    except PermissionError:
        print('Error: You have not got enough permissions.')
        exit()

def main():
    DIR = load_env_vars()    

    config = load_config(config_file='config.json')
    if not config:
        exit()

    file_list = os.listdir(DIR)
    for i in file_list:
        folder_name = check_file(file_name=i, config=config, directory=DIR)
        if folder_name:
            folder_path = os.path.join(DIR,folder_name)
            os.makedirs(folder_path, exist_ok=True)
            move_file(directory=DIR, folder_name=folder_name, file_name=i)

if __name__ == "__main__":
    main()
