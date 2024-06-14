import os
import sqlite3
import socket
import time

class UserFolderCreator:
    """
    Class to create user folders and subfolders based on user ids.
    """

    def __init__(self, db_path, server_address):
        """
        Initialize UserFolderCreator with database file path and server address.

        Args:
        db_path (str): Path to the SQLite database file.
        server_address (tuple): Tuple containing server address and port.
        """
        self.db_path = db_path
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def create_user_folders(self, user_id):
        """
        Create user folder and subfolders if they do not already exist.

        Args:
        user_id (str): The user id for which folders are to be created.
        """
        user_folder = os.path.join(os.getcwd(), str(user_id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
            os.makedirs(os.path.join(user_folder, 'preprocessor'))
            os.makedirs(os.path.join(user_folder, 'DiskSpace'))
            print(f'Folders created for user id: {user_id}')
        else:
            print(f'Folders already exist for user id: {user_id}')

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

    def get_latest_id(self):
        """
        Retrieve the latest user id from the database.

        Returns:
        str: The latest user id.
        """
        select_query = 'SELECT id FROM users ORDER BY id DESC LIMIT 1'
        self.cursor.execute(select_query)
        latest_id = self.cursor.fetchone()
        return latest_id[0] if latest_id else None

if __name__ == '__main__':
    db_path = 'database.db'
    server_address = ('localhost', 12345)  # Change localhost and port as needed

    user_folder_creator = UserFolderCreator(db_path, server_address)
    print('Listening for database changes...')

    try:
        while True:
            latest_id = user_folder_creator.get_latest_id()
            if latest_id:
                user_folder_creator.create_user_folders(latest_id)
                print(f'Folders created for user id: {latest_id}')
            else:
                print('No new id found in the database.')
            time.sleep(1)  # Check for new entries every 5 seconds

    except KeyboardInterrupt:
        print('Stopped by user.')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        user_folder_creator.server_socket.close()
        user_folder_creator.connection.close()
