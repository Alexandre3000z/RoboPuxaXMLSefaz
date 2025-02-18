import requests
from T import TOKEN

#Validação do TOKEN FORNECIDO PELO ADM
def verificar_arquivo(url, texto_procurado):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Gera um erro se a requisição falhar
        conteudo = response.text
        return texto_procurado in conteudo
    except Exception as e:
        print(f"Erro ao acessar o arquivo: {e}")
        return False

# Fluxo principal
def validarAcesso():
    
    url = "https://drive.google.com/uc?export=download&id=1k9Y8YgnsE4KPvQ3_62MdELLj6UhVztsH"
    texto_procurado = TOKEN
    
    if verificar_arquivo(url, texto_procurado):
        
        return True
        # Código autorizado
    else:
        print("Licença não encontrada. Execução não autorizada.")
        return False
    