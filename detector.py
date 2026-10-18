import requests 
from bs4 import BeautifulSoup

site = "https://wosgiftcodes.com/"

def buscar_codigos():
  resposta = requests.get(site, timeout=15)
  resposta.raise_for_status()

  pagina = BeautifulSoup(resposta.text, "html.parser")

  titulo = pagina.find(
    lambda tag: tag.name in ("h2", "h3", "h4", "h5")
    and tag.get_text(strip=True) == "Active Codes"
  )

  if titulo is None:
    raise ValueError("Seção Active Codes não encontrada")

    # Procurar a tabela de códigos ativos
  for elemento in titulo.find_all_next():
    if elemento.name in ("h2", "h3", "h4", "h5"):
      if elemento.get_text(strip=True) == "Expired Codes":
        break

    if elemento.name == "table":
      codigos = []

      for linha in elemento.find_all("tr"):
        coluna = linha.find("td")

        if coluna:
          codigo = coluna.get_text(strip=True)
          codigos.append(codigo)


      return list(dict.fromkeys(codigos))

  return []
