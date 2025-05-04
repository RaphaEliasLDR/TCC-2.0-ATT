
import os
import json

PRATOS_PATH = "pratos.json"
USUARIOS_PATH = "usuarios.json"

def carregar_pratos():
    if not os.path.exists(PRATOS_PATH):
        return []
    with open(PRATOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_pratos(lista_pratos):
    with open(PRATOS_PATH, "w", encoding="utf-8") as f:
        json.dump(lista_pratos, f, indent=4, ensure_ascii=False)

def carregar_usuarios():
    if not os.path.exists(USUARIOS_PATH):
        return []
    with open(USUARIOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_usuarios(lista_usuarios):
    with open(USUARIOS_PATH, "w", encoding="utf-8") as f:
        json.dump(lista_usuarios, f, indent=4, ensure_ascii=False)
