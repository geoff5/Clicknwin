from Crypto.Cipher import AES
import base64
"""Contains function for encrypting and decrypting all database information using the AES algorithm"""


key = "fVJ5YJasSDG3D4Ku"
iv =  "Cw35GddTyBnnuY37"

def encrypt(plain):
    enc = AES.new(key, AES.MODE_CFB, iv)
    cipher = enc.encrypt(plain)
    cipher = base64.b64encode(cipher)
    cipher = cipher.decode("utf-8")
    return cipher

def decrypt(cipher):
    if cipher is None:
        return ""
    enc2 = AES.new(key, AES.MODE_CFB, iv)
    cipher = base64.b64decode(cipher)
    plain = enc2.decrypt(cipher)
    plain = plain.decode("utf-8")
    return plain