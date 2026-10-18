
from playwright.sync_api import sync_playwright

SITE = "https://wos-giftcode.centurygame.com/"

with sync_playwright() as p:

    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    pagina.goto(SITE, wait_until="domcontentloaded")

    # Aguardar o formulário carregar
    pagina.locator("input").first.wait_for(timeout=20000)

    print("\n=== CAMPOS ENCONTRADOS ===")

    campos = pagina.locator("input")

    for i in range(campos.count()):
        campo = campos.nth(i)

        print(f"\nCampo {i + 1}")
        print("Placeholder:", campo.get_attribute("placeholder"))
        print("Tipo:", campo.get_attribute("type"))

    print("\n=== ELEMENTOS CLICÁVEIS ===")

    elementos = pagina.locator(
        "button, [role='button'], "
        "input[type='submit'], [onclick]"
    )

    print("Quantidade encontrada:", elementos.count())

    for i in range(min(elementos.count(), 20)):
        elemento = elementos.nth(i)

        print(f"\nElemento {i + 1}")
        print("Texto:", elemento.text_content())
        print("HTML:", elemento.evaluate(
            "(e) => e.outerHTML.slice(0, 500)"
        ))

    print("\n=== PROCURANDO CONFIRMAR ===")

    botao = pagina.get_by_text("Confirmar", exact=True)

    print("Encontrados:", botao.count())

    if botao.count() > 0:
        print("HTML:", botao.first.evaluate(
            "(e) => e.outerHTML"
        ))

    # Fechar somente depois de toda a inspeção
    input("\nPressione Enter para fechar...")
    navegador.close()
