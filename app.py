import csv
import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
import gerador_hash as gh
import hashlib

def gerar_hash_sha256(texto):
    try:
        with open(texto, 'r', newline='', encoding='utf-8') as f:
            conteudo = f.read()
        # Como alternativa, leia em modo binário para ignorar problemas de quebra de linha:
        # with open(caminho_arquivo, 'rb') as f:
        #     conteudo = f.read()
        hashed = hashlib.sha256(conteudo.encode('utf-8')).hexdigest()
        return hashed
    except Exception as e:
        print(f"Erro ao gerar hash do arquivo: {e}")
        return None


def selecionar_arquivo():
    arquivo = filedialog.askopenfilename()
    return arquivo

def gerar_hash(caminho_arquivo):
    if caminho_arquivo:
        try:
            hash_gerado = gerar_hash_sha256(caminho_arquivo)
            caixa_texto.delete("1.0", ctk.END)
            caixa_texto.insert("1.0", hash_gerado)
            return hash_gerado
        except FileNotFoundError:
            print("Arquivo não encontrado.")
            caixa_texto.delete("1.0", ctk.END)
            caixa_texto.insert("1.0", "Arquivo não encontrado.")
            return None
        except Exception as e:
            print(f"Erro ao gerar hash: {e}")
            caixa_texto.delete("1.0", ctk.END)
            caixa_texto.insert("1.0", f"Erro ao gerar hash: {e}")
            return None
    else:
        caixa_texto.delete("1.0", ctk.END)
        caixa_texto.insert("1.0", "Nenhum arquivo selecionado.")
        return None

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    return pasta

def gerar_hashes_pasta(pasta):
    if pasta:
        try:
            hashes = {}
            for arquivo in os.listdir(pasta):
                caminho_arquivo = os.path.join(pasta, arquivo)
                if os.path.isfile(caminho_arquivo):
                    hash_gerado = gerar_hash_sha256(caminho_arquivo)
                    if hash_gerado:
                        hashes[arquivo] = hash_gerado
                        print(f"Hash de {arquivo}: {hash_gerado}")

            if hashes:
                caixa_texto.delete("1.0", ctk.END)
                for arquivo, hash_gerado in hashes.items():
                    caixa_texto.insert(ctk.END, f"{arquivo}: {hash_gerado}\n")

                if gerar_csv.get():
                    try:
                        caminho_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
                        caminho_csv = os.path.join(caminho_downloads, 'hashes_pastas.csv')
                        with open(caminho_csv, 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            for arquivo, hash_gerado in hashes.items():
                                writer.writerow([pasta, arquivo, hash_gerado])
                        print(f"Hashes salvos em {caminho_csv}")
                        messagebox.showinfo("Sucesso", f"Arquivo CSV salvo em:\n{caminho_csv}")
                    except Exception as e:
                        print(f"Erro ao salvar no CSV: {e}")
                        messagebox.showerror("Erro", f"Erro ao salvar no CSV:\n{e}")
            else:
                caixa_texto.delete("1.0", ctk.END)
                caixa_texto.insert("1.0", "Nenhum arquivo encontrado na pasta.")

            return hashes

        except Exception as e:
            print(f"Erro ao processar pasta: {e}")
            caixa_texto.delete("1.0", ctk.END)
            caixa_texto.insert("1.0", f"Erro ao processar pasta: {e}")
            return None
    else:
        caixa_texto.delete("1.0", ctk.END)
        caixa_texto.insert("1.0", "Nenhuma pasta selecionada.")
        return None

def app():
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.title('Gerador de Hash')
    app.geometry('500x600')

    texto_arquivo = ctk.CTkLabel(app, text='Local do arquivo/pasta:')
    texto_arquivo.pack(pady=10)

    hash_resultado = None
    hashes_resultado = {}

    def armazenar_hash(hash_valor, caminho_arquivo):
        nonlocal hash_resultado
        hash_resultado = hash_valor
        if hash_resultado:
            print(f"Hash armazenado: {hash_resultado}")
            # Exibe o hash na caixa de texto
            caixa_texto.delete("1.0", ctk.END)
            caixa_texto.insert("1.0", hash_resultado)

            if gerar_csv.get():
                try:
                    caminho_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
                    caminho_csv = os.path.join(caminho_downloads, 'hashes.csv')
                    with open(caminho_csv, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([os.path.basename(caminho_arquivo), hash_resultado])
                    print(f"Dados salvos em {caminho_csv}")
                    messagebox.showinfo("Sucesso", f"Arquivo CSV salvo em:\n{caminho_csv}")
                except Exception as e:
                    print(f"Erro ao salvar no CSV: {e}")
                    messagebox.showerror("Erro", f"Erro ao salvar no CSV:\n{e}")
        else:
            print("Nenhum hash foi gerado.")
            caixa_texto.delete("1.0", ctk.END)
            caixa_texto.insert("1.0", "Nenhum hash foi gerado.")

    def armazenar_hashes(hashes_valor, pasta):
        nonlocal hashes_resultado
        hashes_resultado = hashes_valor
        if hashes_resultado:
            print(f"Hashes armazenados: {hashes_resultado}")
            # Exibe os hashes na caixa de texto
            caixa_texto.delete("1.0", ctk.END)
            for arquivo, hash_gerado in hashes_resultado.items():
                caixa_texto.insert(ctk.END, f"{arquivo}: {hash_gerado}\n")

            if gerar_csv.get():
                try:
                    caminho_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
                    caminho_csv = os.path.join(caminho_downloads, 'hashes_pastas.csv')
                    with open(caminho_csv, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        for arquivo, hash_gerado in hashes_resultado.items():
                            writer.writerow([pasta, arquivo, hash_gerado])
                    print(f"Hashes salvos em {caminho_csv}")
                    messagebox.showinfo("Sucesso", f"Arquivo CSV salvo em:\n{caminho_csv}")
                except Exception as e:
                    print(f"Erro ao salvar no CSV: {e}")
                    messagebox.showerror("Erro", f"Erro ao salvar no CSV:\n{e}")
        else:
            print(f"Nenhum hash foi gerado para a pasta: {pasta}")
            caixa_texto.delete("1.0", ctk.END)
            caixa_texto.insert("1.0", "Nenhum hash foi gerado.")

    botao_gerar = ctk.CTkButton(
        master=app,
        text='Gerar Hash SHA256 (Arquivo, unitario)',
        command=lambda: armazenar_hash(gerar_hash(caminho := selecionar_arquivo()), caminho)
    )
    botao_gerar.pack(pady=10)

    botao_gerar_hashes = ctk.CTkButton(
        master=app,
        text='Gerar Hashes de todos os arquivos de uma pasta',
        command=lambda: armazenar_hashes(gerar_hashes_pasta(pasta := selecionar_pasta()), pasta)
    )
    botao_gerar_hashes.pack(pady=10)

    global caixa_texto
    caixa_texto = ctk.CTkTextbox(app, width=300, height=100)
    caixa_texto.pack(pady=10)
    caixa_texto.configure(state="normal")  # Permite que a caixa de texto seja atualizada

    # Checkbox para gerar CSV
    global gerar_csv
    gerar_csv = ctk.BooleanVar(value=True)
    checkbox_csv = ctk.CTkCheckBox(master=app, text="Gerar CSV com os hashes", variable=gerar_csv)
    checkbox_csv.pack(pady=10)

    app.mainloop()

    if hash_resultado:
        print(f"Hash após o mainloop(): {hash_resultado}")

    if hashes_resultado:
        print(f"Hashes após o mainloop(): {hashes_resultado}")

    return hash_resultado, hashes_resultado

app()