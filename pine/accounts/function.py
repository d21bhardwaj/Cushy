from Crypto.Cipher import AES
import base64

MASTER_KEY = "MC4CAQACBQCb16o9AgMBAAECBDKaTqECAwDNFQIDAMKJAgMAvVkCAwCAaQIDALZf"

def encrypt_val(clear_text):
    obj = AES()
    enc_secret = obj.obj(MASTER_KEY[:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.urlsafe_b64encode(enc_secret.encrypt(tag_string))
    return cipher_text.decode("UTF-8")

def decrypt_val(cipher_text):
    cipher_text = bytes(cipher_text,"UTF-8")
    obj = AES
    dec_secret = obj.key(MASTER_KEY[:32])
    raw_decrypted = dec_secret.decrypt(base64.urlsafe_b64decode(cipher_text))
    clear_val = raw_decrypted.decode().rstrip("\0")
    return clear_val