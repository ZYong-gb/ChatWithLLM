import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import dify_settings  # 假设这是你的配置模块（包含 AES_KEY）
import os
from cryptography.exceptions import InvalidTag

# 1. 初始化 AESGCM 对象
def load_aes_key() -> AESGCM:
    key_bytes = base64.b64decode(dify_settings.AES_KEY)  # Base64 → bytes
    return AESGCM(key_bytes)  # 创建 AESGCM 实例

aesgcm = load_aes_key()

# 2. 加密函数 - 返回单个组合字符串
def encrypt_aes_gcm_combined(plaintext: str) -> str:
    """
    使用 AES-GCM 加密明文字符串，返回组合字符串（IV+密文的Base64编码）
    :param plaintext: 明文（字符串）
    :return: Base64编码的字符串（前16字符为IV，后面为密文）
    """
    plaintext_bytes = plaintext.encode("utf-8")
    iv = os.urandom(12)  # 生成12字节随机IV
    ciphertext = aesgcm.encrypt(iv, plaintext_bytes, None)
    # 拼接IV和密文后整体进行Base64编码
    combined = iv + ciphertext
    return base64.b64encode(combined).decode("utf-8")

# 3. 解密函数 - 从组合字符串解密
def decrypt_aes_gcm_combined(combined_base64: str) -> str:
    """
    从组合字符串解密出原始明文
    :param combined_base64: Base64编码的组合字符串（IV+密文）
    :return: 明文（字符串）
    """
    try:
        combined = base64.b64decode(combined_base64)
        iv = combined[:12]  # 前12字节为IV
        ciphertext = combined[12:]  # 剩余部分为密文
        plaintext_bytes = aesgcm.decrypt(iv, ciphertext, None)
        return plaintext_bytes.decode("utf-8")
    except InvalidTag:
        raise ValueError("解密失败：认证标签无效（密钥或数据损坏）")
    except Exception as e:
        raise ValueError(f"解密失败：{str(e)}")