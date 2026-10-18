
import sqlite3
import csv
import sys
from pathlib import Path

from detector import buscar_codigos
from resgatador import processar_pendentes

PASTA = Path(__file__).resolve().parent

# Conectar ao banco de dados
banco = sqlite3.connect(PASTA / "codigos.db")

banco.execute("""
CREATE TABLE IF NOT EXISTS resgate (
    id_amigo TEXT,
    estado TEXT,
    codigo TEXT,
    status TEXT,
    PRIMARY KEY (id_amigo, codigo)
)
""")

try:
    # Modo de resgate
    if "--resgatar" in sys.argv:
        processar_pendentes(banco)

    # Modo de detecção
    else:
        with open(
            PASTA / "amigos.csv",
            encoding="utf-8-sig",
            newline=""
        ) as arquivo:
            amigos = list(csv.DictReader(arquivo))

        codigos = buscar_codigos()

        print(f"Códigos encontrados: {len(codigos)}")

        for codigo in codigos:
            for amigo in amigos:

                id_amigo = amigo["id_amigo"].strip()
                estado = amigo["estado"].strip()

                resultado = banco.execute("""
                    INSERT OR IGNORE INTO resgate
                    (id_amigo, estado, codigo, status)
                    VALUES (?, ?, ?, ?)
                """, (
                    id_amigo,
                    estado,
                    codigo,
                    "pendente"
                ))

                if resultado.rowcount == 1:
                    print(
                        f"Novo resgate: {id_amigo} - {codigo}"
                    )

        banco.commit()

except Exception as erro:
    print(f"Erro: {erro}")
    banco.rollback()

finally:
    banco.close()

