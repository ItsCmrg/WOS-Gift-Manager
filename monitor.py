import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Intervalo entre verificações: 1 hora
INTERVALO = 3600

# Pasta do projeto
PASTA = Path(__file__).resolve().parent

def verificar_codigos():
    agora = datetime.now()

    print(f"\nVerificando códigos: {agora}")

    # Executar o programa principal
    subprocess.run(
        [sys.executable, str(PASTA / "main.py")],
        cwd=PASTA,
        check=True
    )

def iniciar_monitoramento():
    print("WOS Gift Manager iniciado!")

    try:
        while True:
            try:
                verificar_codigos()
            except subprocess.CalledProcessError as erro:
                print(f"Falha na verificação: {erro}")

            # Esperar antes da próxima verificação
            time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")

if __name__ == "__main__":
    iniciar_monitoramento()
