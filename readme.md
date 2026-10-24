
# 🏠 Monitor de Imóveis Automatizado (AI Agent)

Este projeto é um agente de inteligência artificial automatizado que monitora sites de aluguel de imóveis, filtra as melhores oportunidades com base em critérios específicos e envia notificações em tempo real via Telegram.

## 🚀 Como Funciona
O agente opera em um fluxo totalmente automatizado através do **GitHub Actions**, sem a necessidade de um computador ligado:

1. **Busca Web:** Utiliza a API do **Tavily AI** para realizar buscas avançadas em portais imobiliários (Zap Imóveis, VivaReal, OLX, etc).
2. **Análise Inteligente:** Os resultados são enviados para a API da **Groq (Llama 3)**, que atua como o "cérebro", filtrando apenas os anúncios que atendem rigorosamente aos critérios de preço, localização e características.
3. **Notificação:** Se um imóvel relevante for encontrado, o agente envia automaticamente uma mensagem formatada para o **Telegram** do usuário.
4. **Agendamento:** O processo é disparado a cada 1 hora via **GitHub Actions (Cron Job)**.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10
- **LLM:** Groq API (Modelo Llama 3)
- **Busca:** Tavily AI API
- **Notificações:** Telegram Bot API
- **Hospedagem e Automação:** GitHub Actions

## ⚙️ Configuração (Setup)

Para replicar este projeto, é necessário configurar as seguintes variáveis de ambiente nos **Secrets** do repositório do GitHub (`Settings` $\rightarrow$ `Secrets and variables` $\rightarrow$ `Actions`):

| Secret | Descrição | Onde obter |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | Chave da API para a inteligência artificial | [console.groq.com](https://console.groq.com/) |
| `TAVILY_API_KEY` | Chave da API para busca web | [tavily.com](https://tavily.com/) |
| `TELEGRAM_TOKEN` | Token do Bot criado via @BotFather | Telegram |
| `TELEGRAM_CHAT_ID` | ID numérico do usuário | Telegram (@userinfobot) |

## 📁 Estrutura de Arquivos
- `main.py`: Contém a lógica de busca, análise da IA e envio de mensagens.
- `.github/workflows/schedule.yml`: Arquivo de configuração que agenda a execução do robô a cada hora.

## 📝 Manutenção e Ajustes
Para alterar os critérios de busca (Cidade, Preço, Quartos), basta editar a variável `FILTROS_BUSCA` dentro do arquivo `main.py`.

**Exemplo de filtro:**
`"aluguel de imóveis em Niterói RJ, máximo 2500 reais, 2 quartos, sites Zap Imóveis, VivaReal, OLX"`

---
*Desenvolvido com auxílio de IA para automação de busca imobiliária.*
