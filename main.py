import gerador_hash

arquivo = input('Digite o arquivo: ')


resultado = gerador_hash.gerar_hash_sha256(arquivo)

print(resultado)