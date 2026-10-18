
import sqlite3
from playwright.sync_api import sync_playwright

SITE = "https://wos-giftcode.centurygame.com/"

# Buscar até 10 resgates pendentes
banco = sqlite3.connect("codigos.db")

pendentes = banco.execute("""
    SELECT id_amigo, estado, codigo
    FROM resgate
    WHERE status = 'pendente'
    LIMIT 10
""").fetchall()

banco.close()


if not pendentes:
    print("Nenhum resgate pendente.")

else:
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)
        pagina = navegador.new_page()

        try:
            for id_amigo, estado, codigo in pendentes:
                pagina.goto(
                    SITE,
                    wait_until="domcontentloaded"
                )

                # Preencher formulário
                pagina.get_by_placeholder(
                    "ID do Jogador"
                ).fill(id_amigo)

                pagina.get_by_placeholder(
                    "Estado"
                ).fill(estado)

                pagina.get_by_placeholder(
                    "Inserir Código de Presente"
                ).fill(codigo)

                # Consultar estado do botão
                botao = pagina.locator("div.exchange_btn")
                classe = botao.get_attribute("class") or ""

                print(f"\nJogador: {id_amigo}")
                print(f"Código: {codigo}")
                print(f"Classe do botão: {classe}")

                if "disabled" in classe.split():
                    print("Botão ainda marcado como desabilitado.")
                else:
                    print("Classe disabled não encontrada.")

                input(
                    "Confira o preenchimento, sem confirmar. "
                    "Pressione Enter para o próximo..."
                )

        finally:
            navegador.close()
