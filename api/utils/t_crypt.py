#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: t_crypt.py
@time: 2025/7/22 15:34
@project: resonant-soul
@desc: 实现基于 AES 的 API Key 加解密功能
"""

import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from api.utils import file_utils


def generate_key():
    """
    生成一个 256 位的 AES 密钥
    :return: 生成的密钥
    """
    # 生成随机的 256 位密钥
    file_path = os.path.join(
        file_utils.get_project_base_directory(),
        "conf",
        "public.pem")
    # 以二进制模式读取文件，确保返回 bytes 类型
    with open(file_path, 'rb') as f:
        key_val = f.read()
    key_val = key_val[:32]
    return key_val


def encrypt_api_key(api_key, key):
    """
    使用 AES 算法对 API Key 进行加密
    :param api_key: 待加密的 API Key
    :param key: 加密密钥
    :return: 加密后的 Base64 编码字符串
    """
    # 生成随机的初始化向量 (IV)
    iv = os.urandom(16)
    # 创建 AES 加密器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # 使用 PKCS7 填充
    padder = padding.PKCS7(128).padder()
    # 对 API Key 进行编码和填充
    padded_data = padder.update(api_key.encode()) + padder.finalize()
    # 加密数据
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    # 将 IV 和加密数据组合并进行 Base64 编码
    return base64.b64encode(iv + encrypted_data).decode()


def decrypt_api_key(encrypted_api_key, key):
    """
    使用 AES 算法对加密的 API Key 进行解密
    :param encrypted_api_key: 加密后的 Base64 编码字符串
    :param key: 解密密钥
    :return: 解密后的 API Key
    """
    # 对 Base64 编码的字符串进行解码
    decoded_data = base64.b64decode(encrypted_api_key)
    # 提取 IV 和加密数据
    iv = decoded_data[:16]
    encrypted_data = decoded_data[16:]
    # 创建 AES 解密器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    # 解密数据
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    # 使用 PKCS7 解填充
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    # 将解密后的数据解码为字符串
    return unpadded_data.decode()
