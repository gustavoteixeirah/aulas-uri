"""Monta o `dados/corridas-2019.csv` a partir dos arquivos públicos do TLC de NY.

Não precisa rodar para a aula: o arquivo já está na pasta, com 8 KB e 365 linhas
— uma por dia de 2019, com a contagem de corridas e a tarifa média do dia. Rode
só se quiser refazê-lo.

Baixa os doze meses de táxi amarelo de 2019 (84,6 milhões de corridas, uns
poucos minutos) lendo **duas colunas** de cada arquivo: parquet é colunar, então
o resto nem vem pela rede.

Uso:  python baixa-ano-2019.py
"""
import os

import pandas as pd

URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2019-{:02d}.parquet"
SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados", "corridas-2019.csv")

partes = []
for mes in range(1, 13):
    t = pd.read_parquet(URL.format(mes), columns=["tpep_pickup_datetime", "fare_amount"])
    t.columns = ["pickup", "fare"]
    # o arquivo de cada mês traz corridas datadas de outros meses — e algumas de
    # 2001, 2008, 2020. O recorte do ano é feito aqui, e os dias que aparecem em
    # mais de um arquivo se juntam depois.
    t = t[(t["pickup"] >= "2019-01-01") & (t["pickup"] < "2020-01-01")]
    partes.append(t.groupby(t["pickup"].dt.normalize())
                   .agg(corridas=("fare", "size"), soma=("fare", "sum")))
    print(f"mês {mes:02d}: {len(t):>10,} corridas", flush=True)

ano = pd.concat(partes).groupby(level=0).sum()        # um único registro por dia
ano["tarifa_media"] = (ano["soma"] / ano["corridas"]).round(2)
ano.index.name = "dia"
ano[["corridas", "tarifa_media"]].to_csv(SAIDA)

mes_a_mes = ano["corridas"].resample("ME").sum()
print(f"\n{len(ano)} dias · {int(ano['corridas'].sum()):,} corridas")
print("mês mais forte:", mes_a_mes.idxmax().strftime("%m/%Y"), f"{mes_a_mes.max():,}")
print("mês mais fraco:", mes_a_mes.idxmin().strftime("%m/%Y"), f"{mes_a_mes.min():,}")
print("menor dia:", ano["corridas"].idxmin().date(), f"{int(ano['corridas'].min()):,}")
