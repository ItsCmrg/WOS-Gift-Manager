
from playwright.sync_api import sync_playwright
from resultado import interpretar_resultado

SITE = "https://wos-giftcode.centurygame.com/"

# Manter False enquanto o envio automático
# não estiver autorizado
ENVIO_AUTOMATICO = False


def iniciar_captura(pagina):
    pagina.evaluate("""
    () => {
        window.__wosMensagens = [];

        function guardar(texto) {
            texto = (texto || "").trim();

            if (
                texto &&
                texto.length <= 300 &&
                !window.__wosMensagens.includes(texto)
            ) {
                window.__wosMensagens.push(texto);
            }
        }

        const observador = new MutationObserver(alteracoes => {
            for (const alteracao of alteracoes) {

                if (alteracao.type === "characterData") {
                    guardar(alteracao.target.textContent);
                }

                if (alteracao.type === "attributes") {
                    guardar(alteracao.target.textContent);
                }

                for (const elemento of alteracao.addedNodes) {
                    guardar(elemento.textContent);

                    if (elemento.nodeType === 1) {
                        for (const filho of elemento.querySelectorAll(
                            "div, span, p"
                        )) {
                            guardar(filho.textContent);
                        }
                    }
                }
            }
        });

        observador.observe(document.body, {
            childList: true,
            characterData: true,
            attributes: true,
            attributeFilter: ["class", "style"],
            subtree: true
        });
    }
    """)


def verificar_mensagens(pagina):
    mensagens = pagina.evaluate(
        "() => window.__wosMensagens || []"
    )

    for mensagem in reversed(mensagens):
        status = interpretar_resultado(mensagem)

        if status is not None:
            return status

    print("Mensagens observadas:", mensagens[-10:])
    return "revisar"


def resgatar_codigo(pagina, id_amigo, estado, codigo):

    pagina.goto(SITE, wait_until="domcontentloaded")

    # Preencher os três campos
    pagina.get_by_placeholder(
        "ID do Jogador"
    ).fill(id_amigo)

    pagina.get_by_placeholder(
        "Estado"
    ).fill(estado)

    pagina.get_by_placeholder(
        "Inserir Código de Presente"
    ).fill(codigo)

    # Esperar o botão ficar disponível
    botao = pagina.locator(
        "div.exchange_btn:not(.disabled)"
    )

    botao.wait_for(state="visible", timeout=15000)

    print(f"Formulário preparado: {id_amigo}")
    iniciar_captura(pagina)
    if ENVIO_AUTOMATICO:
        botao.click()
    else:
        confirmou = input(
            "Confirme manualmente no navegador. "
            "Digite 'ok' após clicar, "
            "ou Enter para pular: "
        ).strip().lower()

        if confirmou != "ok":
            return None

    
      # Aguardar uma resposta reconhecida por até 10 segundos
    for tentativa in range(20):

      mensagens = pagina.evaluate(
            "() => window.__wosMensagens || []"
        )

      for mensagem in reversed(mensagens):
        status = interpretar_resultado(mensagem)

        if status is not None:
            print(f"Resultado identificado: {status}")
            return status

      pagina.wait_for_timeout(500)

    print("Nenhuma confirmação reconhecida.")

    # Recuperar mensagens exibidas pelo site
    mensagens = pagina.evaluate(
        "() => window.__wosMensagens || []"
    )

    # Registrar mensagens desconhecidas para análise
    with open(
        "mensagens_wos.log",
        "a",
        encoding="utf-8"
    ) as arquivo:
        arquivo.write(
            f"\nJogador: {id_amigo} | Código: {codigo}\n"
        )

        for mensagem in mensagens:
            arquivo.write(f"{mensagem}\n")

    print("Mensagens registradas em mensagens_wos.log")

    return "revisar"




def processar_pendentes(banco):

    pendentes = banco.execute("""
        SELECT id_amigo, estado, codigo
        FROM resgate
        WHERE status = 'pendente'
        LIMIT 10
    """).fetchall()

    if not pendentes:
        print("Nenhum resgate pendente.")
        return

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)
        pagina = navegador.new_page()

        try:
            for id_amigo, estado, codigo in pendentes:
                try:
                    status = resgatar_codigo(
                        pagina, id_amigo, estado, codigo
                    )

                    if status is None:
                        print("Resgate não enviado.")
                        continue

                    banco.execute("""
                        UPDATE resgate
                        SET status = ?
                        WHERE id_amigo = ? AND codigo = ?
                    """, (status, id_amigo, codigo))

                    banco.commit()
                    print(f"ID {id_amigo}: {status}")

                except Exception as erro:
                    print(f"Falha no ID {id_amigo}: {erro}")
                    print("Verifique antes de repetir.")
                    break
        finally:
            navegador.close()
