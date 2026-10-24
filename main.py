import os
import requests
from groq import Groq
from tavily import TavilyClient

# ================= CONFIGURAÇÕES DE SEGURANÇA =================
# O código agora busca as chaves nos "Secrets" do GitHub
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Filtros de busca (Você pode editar este texto aqui no GitHub mesmo)
FILTROS_BUSCA = "aluguel de imóveis em Niterói RJ, máximo 2500 reais, 2 quartos, sites Zap Imóveis, VivaReal, OLX"
# ==============================================================

# Inicializando as ferramentas
groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def buscar_imoveis():
    busca = tavily_client.search(query=FILTROS_BUSCA, search_depth="advanced", max_results=5)
    return busca['results']

def analisar_com_ia(resultados):
    contexto = "\n".join([f"Título: {r['title']}\nURL: {r['url']}\nConteúdo: {r['content']}" for r in resultados])
    prompt = f"Analise os seguintes resultados de busca: {contexto}. Filtros: {FILTROS_BUSCA}. Se encontrar imóveis relevantes, retorne os links e resumo. Se não, responda apenas: 'NADA_ENCONTRADO'."
    
    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b", # Verifique se este modelo continua ativo
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
    requests.post(url, json=payload)

# EXECUÇÃO
if __name__ == "__main__":
    imoveis = buscar_imoveis()
    analise = analisar_com_ia(imoveis)

    if "NADA_ENCONTRADO" not in analise:
        enviar_telegram(f"🏠 *Novos Imóveis Encontrados!*\n\n{analise}")
