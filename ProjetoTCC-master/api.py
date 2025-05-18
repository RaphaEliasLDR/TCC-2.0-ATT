import requests

API_URL = "http://localhost:3000/pratos"
API_TOKEN = "seu_token_aqui"  # Remova se não usar autenticação


def enviar_prato_para_api(nome: str, preco: str, categoria: str, imagem_path: str):
    
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    data = {
        "nome": nome,
        "preco": preco,
        "categoria": categoria
    }

    try:
        with open(imagem_path, "rb") as imagem_file:
            files = {"imagem": imagem_file}
            response = requests.post(API_URL, data=data, files=files, headers=headers)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", response.status_code)
        print("Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar dados para a API:", e)
    return None

'''
def atualizar_prato_api(id_prato: str, nome: str, preco: str, categoria: str, imagem_path: str = None):
    import requests

    url = f"http://localhost:3000/pratos-json/{id_prato}"
    headers = {
        "Content-Type": "application/json"
    }

    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"

    data = {
        "nome": nome,
        "preco": preco,
        "categoria": categoria
    }

    # Se a imagem for um caminho ou nome de arquivo, pode incluir como string opcional
    if imagem_path:
        data["imagem"] = imagem_path

    try:
        print("➡️ Enviando dados para API (JSON):", data)
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        print("✅ Resposta da API:", response.json())
        return response.json()
    except requests.exceptions.HTTPError:
        print("❌ Erro HTTP:", response.status_code)
        print("❌ Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao enviar dados para a API:", e)
    return None
'''
'''
def atualizar_prato_api(id_prato: str, nome: str, preco: str, categoria: str, imagem_path: str = None):
    import mimetypes
    url = f"http://localhost:3000/pratos/{id_prato}"
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    data = {
        "nome": nome,
        "preco": str(preco),
        "categoria": categoria
    }

    files = None
    file_obj = None
    try:
        if imagem_path:
            mime_type = mimetypes.guess_type(imagem_path)[0] or 'application/octet-stream'
            file_obj = open(imagem_path, "rb")
            files = {'imagem': (imagem_path, file_obj, mime_type)}

        response = requests.put(url, data=data, files=files, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError:
        print("Erro HTTP:", response.status_code)
        print("Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar dados para a API:", e)
    finally:
        if file_obj:
            file_obj.close()

    return None
'''

def atualizar_prato_api(id_prato: str, nome: str, preco: str, categoria: str, imagem_path: str = None):
    import requests
    import mimetypes

    url = f"http://localhost:3000/pratos/{id_prato}"
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    data = {
        "nome": nome,
        "preco": str(preco),
        "categoria": categoria
    }

    try:
        if imagem_path:
            mime_type = mimetypes.guess_type(imagem_path)[0] or 'application/octet-stream'
            with open(imagem_path, "rb") as file_obj:
                files = {'imagem': (imagem_path, file_obj, mime_type)}
                response = requests.put(url, data=data, files=files, headers=headers)
        else:
            response = requests.put(url, data=data, headers=headers)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError:
        print("Erro HTTP:", response.status_code)
        print("Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar dados para a API:", e)

    return None


def listar_pratos_da_api():
    headers = {}
    if API_TOKEN:
        headers['Authorization'] = f"Bearer {API_TOKEN}"

    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", response.status_code)
        print("Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao buscar pratos na API:", e)
    return []

import requests

def deletar_prato_api(id_prato: str):
    url = f"http://localhost:3000/pratos/{id_prato}"
    try:
        response = requests.delete(url)
        response.raise_for_status()
        print("Prato deletado com sucesso:", response.json())
        return True
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", response.status_code)
        print("Resposta da API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao deletar prato na API:", e)
    return False
