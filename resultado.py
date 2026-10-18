
import unicodedata

def normalizar(texto):
    texto = texto.lower()

    return "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caractere) != "Mn"
    )


def interpretar_resultado(mensagem):
    texto = normalizar(mensagem)

    if any(frase in texto for frase in [
        "ja resgatado",
        "ja utilizado",
        "already claimed",
        "already redeemed"
    ]):
        return "ja_resgatado"

    if any(frase in texto for frase in [
        "codigo expirado",
        "codigo expirou",
        "expired, unable to claim"
    ]):
        return "expirado"

    if any(frase in texto for frase in [
        "codigo invalido",
        "codigo nao encontrado",
        "gift code not found"
    ]):
        return "invalido"

    if any(frase in texto for frase in [
        "resgatado com sucesso",
        "resgate realizado com sucesso",
        "successfully redeemed",
        "redeemed successfully"
    ]):
        return "sucesso"

    return None
