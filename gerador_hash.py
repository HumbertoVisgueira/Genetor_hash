import hashlib

def gerar_hash_sha256(texto):
    #criando um objeto hash SHA-256
    sha256= hashlib.sha256()

    #Atualizando o objeto hash com texto (convertido para hash)
    sha256.update(texto.encode('utf-8'))

    #Retornar o hash gerado em formato hexadecimal
    return sha256.hexdigest()

