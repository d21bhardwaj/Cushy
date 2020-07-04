from Crypto.Cipher import AES
import base64

MASTER_KEY = "MC4CAQACBQCb16o9AgMBAAECBDKaTqECAwDNFQIDAMKJAgMAvVkCAwCAaQIDALZf"

def encrypt_val(clear_text):
    enc_secret = AES.new(MASTER_KEY[:32],AES.MODE_EAX)
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.urlsafe_b64encode(enc_secret.encrypt(tag_string))
    return cipher_text.decode("UTF-8")

def decrypt_val(cipher_text):
    cipher_text = bytes(cipher_text,"UTF-8")
    dec_secret = AES.new(MASTER_KEY[:32],AES.MODE_EAX)
    raw_decrypted = dec_secret.decrypt(base64.urlsafe_b64decode(cipher_text))
    clear_val = raw_decrypted.decode().rstrip("\0")
    return clear_val