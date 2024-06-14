import sqlite3
import os
import boto3

class S3Uploader:
    def __init__(self, access_key, secret_key, bucket_name):
        self.s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.bucket_name = bucket_name

    def upload_latest_mp3(self, directory_path, user_id):
        if os.path.exists(directory_path):
            mp3_files = [file for file in os.listdir(directory_path) if file.endswith('.mp3') and file.startswith('final')]
            print(f'Files in {directory_path}: {mp3_files}')
            
            if mp3_files:
                latest_file = max(mp3_files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
                print(f'Latest .mp3 file in {directory_path}: {latest_file}')
                
                file_path = os.path.join(directory_path, latest_file)
                if os.path.isfile(file_path):
                    print(f'Uploading {latest_file} to S3 bucket {self.bucket_name}')
                    self.s3.upload_file(file_path, self.bucket_name, latest_file)
                    print(f'{latest_file} uploaded to S3 bucket {self.bucket_name}')
                else:
                    print(f'File {latest_file} does not exist in {directory_path}')
            else:
                print(f'No .mp3 files found in {directory_path} starting with "final"')
        else:
            print(f'Directory {directory_path} does not exist for user_id {user_id}')

# AWS credentials and bucket name
ACCESS_KEY = 'AKIA4MTWIY55JXA3F3I6'
SECRET_KEY = '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'
BUCKET_NAME = 'mfs-mcee'

# Initialize S3Uploader
uploader = S3Uploader(ACCESS_KEY, SECRET_KEY, BUCKET_NAME)

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Query the users table and iterate over the id column
cursor.execute('SELECT id FROM users')
for row in cursor.fetchall():
    user_id = row[0]
    directory_path = f'/home/ec2-user/{user_id}'
    uploader.upload_latest_mp3(directory_path, user_id)

# Close the database connection
conn.close()
