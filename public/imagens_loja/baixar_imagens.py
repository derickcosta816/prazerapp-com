from serpapi import GoogleSearch
import pandas as pd
import pathlib, requests, os, time
from dotenv import load_dotenv

# ──────────────────────────────────────────────────────────────────────────────
# 1) Lê variáveis do arquivo .env
# ──────────────────────────────────────────────────────────────────────────────
load_dotenv()                                 # procura .env na pasta atual
KEY = os.getenv("SERP_KEY")                   # sua chave da SerpAPI

if not KEY:
    raise RuntimeError(
        "Variável SERP_KEY não encontrada. "
        "Crie um arquivo .env com a linha:  SERP_KEY=<sua_chave_aqui>"
    )

# ──────────────────────────────────────────────────────────────────────────────
# 2) Lê a lista de produtos e prepara a pasta-raiz
# ──────────────────────────────────────────────────────────────────────────────
df   = pd.read_csv("product_image_queries.csv")
root = pathlib.Path("imgs_google")
root.mkdir(exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────────
# 3) Percorre cada produto, consulta a API e salva as 5 primeiras imagens
# ──────────────────────────────────────────────────────────────────────────────
for _, row in df.iterrows():
    pasta = root / row.slug
    pasta.mkdir(exist_ok=True)

    print(f"📥  Baixando: {row.product_name}")

    params = {
        "engine": "google",
        "q": row.product_name,
        "tbm": "isch",
        "num": 5,
        "api_key": KEY,
    }
    dados = GoogleSearch(params).get_dict()

    for i, img in enumerate(dados.get("images_results", [])[:5], start=1):
        url = img["original"]
        ext = url.split(".")[-1].split("?")[0][:4] or "jpg"
        destino = pasta / f"{i}.{ext}"

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            destino.write_bytes(resp.content)
        except Exception as e:
            print(f"   ⚠️  Erro ao baixar {url[:60]}... -> {e}")
            continue

    time.sleep(0.25)          # respeita limite da API gratuita

print("\n✅  Concluído! Veja as imagens em imgs_google/<slug>/")