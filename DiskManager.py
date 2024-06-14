import os
import sqlite3
import socket
import time
import shutil

class UserFolderCreator:
    """
    Class to create user folders and subfolders based on user ids and manage folder contents.
    """

    def __init__(self, db_path, server_address, base_url):
        """
        Initialize UserFolderCreator with database file path, server address, and base URL.

        Args:
        db_path (str): Path to the SQLite database file.
        server_address (tuple): Tuple containing server address and port.
        base_url (str): Base URL where user folders are located.
        """
        self.db_path = db_path
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.base_url = base_url

    def create_user_folders(self, user_id):
        """
        Create user folder and subfolders if they do not already exist.

        Args:
        user_id (str): The user id for which folders are to be created.
        """
        user_folder = os.path.join(self.base_url, str(user_id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
            os.makedirs(os.path.join(user_folder, 'preprocessor'))
            os.makedirs(os.path.join(user_folder, 'DiskSpace'))
            print(f'Folders created for user id: {user_id}')
        else:
            print(f'Folders already exist for user id: {user_id}')
            self.manage_folders(user_folder)

    def manage_folders(self, user_folder):
        """
        Manage folders by checking DiskSpace and clearing preprocessor if needed.

        Args:
        user_folder (str): The path to the user's folder.
        """
        disk_space_folder = os.path.join(user_folder, 'DiskSpace')
        preprocessor_folder = os.path.join(user_folder, 'preprocessor')

        if os.listdir(disk_space_folder):
            print(f'DiskSpace folder is not empty for user folder: {user_folder}')
            self.clear_folder(preprocessor_folder)
        else:
            print(f'DiskSpace folder is empty for user folder: {user_folder}')

    def clear_folder(self, folder_path):
        """
        Clear all contents of a folder.

        Args:
        folder_path (str): The path to the folder to be cleared.
        """
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        print(f'Cleared contents of folder: {folder_path}')

    def start_server(self):
        """
        Start the server socket to listen for incoming connections.
        """
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(1)
        print('Listening for incoming connections...')
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                data = client_socket.recv(1024)
                client_socket.close()
        finally:
            self.server_socket.close()

    def get_all_ids(self):
        """
        Retrieve all user ids from the database.

        Returns:
        list: A list of all user ids.
        """
        select_query = 'SELECT id FROM users'
        self.cursor.execute(select_query)
        all_ids = self.cursor.fetchall()
        return [user_id[0] for user_id in all_ids] if all_ids else []

if __name__ == '__main__':
    db_path = 'database.db'
    server_address = ('localhost', 12345)  # Change localhost and port as needed
    base_url = 'C:\\Users\\HomePC\\Desktop\\Litespeed'

    user_folder_creator = UserFolderCreator(db_path, server_address, base_url)
    print('Listening for database changes...')

    try:
        while True:
            user_ids = user_folder_creator.get_all_ids()
            if user_ids:
                for user_id in user_ids:
                    user_folder_creator.create_user_folders(user_id)
                    print(f'Processed folders for user id: {user_id}')
            else:
                print('No user ids found in the database.')
            time.sleep(600)  # Check for new entries every 600 seconds

    except KeyboardInterrupt:
        print('Stopped by user.')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        user_folder_creator.server_socket.close()
        user_folder_creator.connection.close()
