import os
import requests
from groq import Groq
from tavily import TavilyClient
from firecrawl import FirecrawlApp

# ================= CONFIGURAÇÕES DE SEGURANÇA =================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

FILTROS_BUSCA = "aluguel de imóveis em Niterói RJ, máximo 2500 reais, 2 quartos, Zap Imóveis ou VivaReal"
# ==============================================================

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def buscar_paginas_listagem():
    # Busca páginas que contenham as listas de imóveis
    busca = tavily_client.search(query=FILTROS_BUSCA, search_depth="advanced", max_results=3)
    return [r['url'] for r in busca['results']]

def extrair_links_individuais(url_listagem):
    # O resultado agora é um objeto 'Document'
    scrape_result = firecrawl.scrape(url_listagem, formats=['markdown'])
    
    # CORREÇÃO: Trocado ['markdown'] por .markdown
    content = scrape_result.markdown[:10000] 
    
    prompt_extrair = f"Extraia apenas as URLs de anúncios individuais de imóveis deste texto: {content}. Retorne apenas as URLs separadas por vírgula. Se não houver links de imóveis, responda 'NENHUM'."
    
    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt_extrair}]
    )
    res = completion.choices[0].message.content
    return [link.strip() for link in res.split(",") if "http" in link] if "NENHUM" not in res else []

def analisar_imovel(url_imovel):
    # O resultado agora é um objeto 'Document'
    detalhes = firecrawl.scrape(url_imovel, formats=['markdown'])
    
    # CORREÇÃO: Trocado ['markdown'] por .markdown
    content = detalhes.markdown[:5000]
    
    prompt_analise = f"Analise este imóvel: {content}. Filtros: {FILTROS_BUSCA}. Se for compatível, resuma: Título, Preço e link {url_imovel}. Se não for compatível, responda 'NADA_ENCONTRADO'."
    
    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt_analise}]
    )
    return completion.choices[0].message.content
    
def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# EXECUÇÃO
if __name__ == "__main__":
    urls_listagem = buscar_paginas_listagem()
    todos_imoveis_encontrados = []

    for url in urls_listagem:
        links_individuais = extrair_links_individuais(url)
        for link in links_individuais[:5]: # Analisa no máximo 5 por página para não gastar tokens
            resultado = analisar_imovel(link)
            if "NADA_ENCONTRADO" not in resultado:
                todos_imoveis_encontrados.append(resultado)

    if todos_imoveis_encontrados:
        mensagem_final = "🏠 *Imóveis Filtrados com Precisão:*\n\n" + "\n\n".join(todos_imoveis_encontrados)
        enviar_telegram(mensagem_final)
