import os
import requests

def enviar_resgate(id_amigo, estado, codigo):
    url = os.getenv("REDEEM_API_URL")

    # Sem uma API autorizada, não enviar requisições
    if not url:
        return None

    dados = {
        "player_id": id_amigo,
        "state": estado,
        "gift_code": codigo
    }

    resposta = requests.post(
        url,
        json=dados,
        timeout=15
    )

    resposta.raise_for_status()

    resultado = resposta.json()
    return resultado
