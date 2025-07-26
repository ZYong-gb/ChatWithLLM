import os
import base64


# 1. 生成 AES-256 密钥
def generate_aes_gcm_key(key_size: int = 32) -> bytes:
    """
    生成指定长度的 AES-GCM 密钥（字节串）。
    :param key_size: 16（AES-128）、24（AES-192）、32（AES-256）
    :return: 密钥（bytes）
    """
    if key_size not in (16, 24, 32):
        raise ValueError("Key size must be 16, 24, or 32 bytes")
    return os.urandom(key_size)


# 2. 将密钥转换为 Base64 字符串（便于存储到环境变量）
def b64encode_generated_key(generated_key: bytes) ->str:
    key_base64 = base64.b64encode(generated_key).decode()
    # print("Base64 编码的密钥:", key_base64)
    return key_base64


# 只运行一次，确保全流程中密钥统一
if __name__ == "__main__":
    generated_key = generate_aes_gcm_key()
    key_base64 = b64encode_generated_key(generated_key)
    print("编码后的密钥：",key_base64) # 需要手动保存到环境变量中（.env）