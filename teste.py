import hashlib

def hash_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', newline='', encoding='utf-8') as f:
            conteudo = f.read()
        # Como alternativa, leia em modo binário para ignorar problemas de quebra de linha:
        # with open(caminho_arquivo, 'rb') as f:
        #     conteudo = f.read()
        hashed = hashlib.sha256(conteudo.encode('utf-8')).hexdigest()
        return hashed
    except Exception as e:
        print(f"Erro ao gerar hash do arquivo: {e}")
        return None

# Exemplo de uso:
caminho_arquivo1 = "/home/humberto.visgueira/Documentos/teste 1 (cópia)/Teste 2 - Página1 (cópia).csv"
caminho_arquivo2 = "/home/humberto.visgueira/Documentos/teste 1/Teste 2 - Página1 (cópia).csv"

hash1 = hash_arquivo(caminho_arquivo1)
hash2 = hash_arquivo(caminho_arquivo2)

if hash1 == hash2:
    print("Hashes correspondem!")
else:
    print("Hashes diferem.")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
