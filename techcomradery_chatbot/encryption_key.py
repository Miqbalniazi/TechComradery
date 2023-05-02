def decrypt(cipher_text):
    _str = ""
    for i in cipher_text:
        _str += chr(ord(i) - 5)
    
    return _str