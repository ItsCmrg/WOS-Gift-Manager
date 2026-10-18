# WOS Gift Manager

Sistema desenvolvido em Python para gerenciar gift codes do Whiteout Survival.

## Funcionalidades

- Detecção de gift codes em fontes configuradas.
- Gerenciamento de múltiplos jogadores por CSV.
- Armazenamento de códigos e resultados com SQLite.
- Preenchimento de formulários utilizando Playwright.
- Interpretação e registro de respostas do resgate.
- Monitoramento periódico configurável.

## Tecnologias

Python, SQLite, Requests, BeautifulSoup e Playwright.

## Instalação

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Crie um arquivo `amigos.csv` com as colunas `id_amigo,estado` e os dados dos jogadores que autorizaram sua inclusão.

## Execução

Detecção de códigos:

```bash
python main.py
```

Processamento assistido de resgates:

```bash
python main.py --resgatar
```

## Estado do projeto

Protótipo em desenvolvimento. O preenchimento automático do formulário foi verificado, mas a detecção e a confirmação de resgates reais ainda precisam de validação.

O envio automático sem intervenção permanece desativado enquanto sua autorização não estiver confirmada.
