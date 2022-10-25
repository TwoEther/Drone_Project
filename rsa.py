from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import aes

def createPEM(abb):
    private_key = RSA.generate(1024)
    filename = abb + 'privatekey.pem'
    with open(filename, 'wb+') as f:
        f.write(private_key.export_key('PEM'))

    filename = abb + 'publickey.pem'
    public_key = private_key.publickey()
    with open(filename, 'wb+') as f:
        f.write(public_key.export_key('PEM'))

def readPEM(pemfile):
    with open(pemfile, 'r') as f:
        key = RSA.importKey(f.read())
    return key

def rsa_enc(msg, filename):
    with open(filename, 'r') as f:
        key = RSA.importKey(f.read())
    
    key = readPEM(filename)
    cipher = PKCS1_OAEP.new(key)
    encdata = cipher.encrypt(msg)
    return encdata

def rsa_dec(msg, filename):
    private_key = readPEM(filename)
    cipher = PKCS1_OAEP.new(private_key)
    try:
        decdata = cipher.decrypt(msg)
    except ValueError or TypeError:
        return False
    else:
        return decdata
    
def view_rsa_dec(msg, fil):
    pass


if __name__ == "__main__":
    msg = 'samsjang~1234'
    createPEM('W_')
    ciphered = rsa_enc(msg.encode(), 'W_publickey.pem')
    print(ciphered)
    deciphered = rsa_dec(ciphered, 'W_privatekey.pem')
    print(deciphered)