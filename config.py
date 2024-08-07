import os 

prod = os.environ.get('PRODUCTION', None)
suffix = os.environ.get("RABBITMQ_SUFFIX", "")
url = os.environ.get("RABBITMQ_URL", None)
host= os.environ.get('MONGODB_HOST', None)
username= os.environ.get('MONGODB_USER', None)
password= os.environ.get('MONGODB_PASS', None)
db_name = os.environ.get('MONGODB_DATABASE', None)
AZURE_STORAGE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME', None)
AZURE_STORAGE_ACCOUNT_KEY = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY', None)
AZURE_CONTAINER_NAME = os.environ.get('AZURE_CONTAINER_NAME', None)
REDIS_HOST = os.environ.get('REDIS_HOST', "redis")
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
REDIS_EXPIRE_MINUTES = int(os.environ.get('REDIS_EXPIRE_MINUTES', 60))
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = os.environ.get("SMTP_PORT")
EMAIL = os.environ.get("EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EXP_TIME_IN_MIN = int(os.environ.get("EXP_TIME_IN_MIN",60))

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 10080)) # 7 days
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
SECRET_KEY = os.environ.get("SECRET_KEY", "secret_key")
ENCRYPT_DECRYPT_SECRET_KEY = os.environ.get("ENCRYPT_DECRYPT_SECRET_KEY")

send_email_req_data = {
    "SMTP_SERVER":SMTP_SERVER,
    "SMTP_PORT":SMTP_PORT,
    "EMAIL":EMAIL,
    "EMAIL_PASSWORD":EMAIL_PASSWORD,
}

#TODO: Move below code into package.
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt(field_to_encrypt):
    try:
        key = ENCRYPT_DECRYPT_SECRET_KEY.encode('utf-8')  # 16 bytes key for AES-128
        cipher = AES.new(key, AES.MODE_CBC, iv=b'1234567890123456')  # Fixed IV
        padded_data = pad(field_to_encrypt.encode('utf-8'), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode('utf-8')
    except:
        raise

def decrypt(encrypted_field):
    try:
        key = ENCRYPT_DECRYPT_SECRET_KEY.encode('utf-8')  # 16 bytes key for AES-128
        cipher = AES.new(key, AES.MODE_CBC, iv=b'1234567890123456')  # Fixed IV
        encrypted_data = base64.b64decode(encrypted_field)
        decrypted_data = cipher.decrypt(encrypted_data)
        return unpad(decrypted_data, AES.block_size).decode('utf-8')
    except Exception as e:
        raise e
