# 🛡️ GDPR / LGPD Compliance Checker

Uma ferramenta web que audita sites automaticamente em busca de violações à LGPD (Brasil) e GDPR (Europa).

## 🔍 Funcionalidades

- ✅ **Scanner de Cookies e Rastreadores**
  - Detecta cookies como Google Analytics, Meta Pixel, etc.
  - Classifica por tipo: marketing, análise, funcional.
  - Verificação com Selenium e requests.

- 🔐 **Verificador de SSL/TLS**
  - Avalia força da criptografia do site.
  - Identifica uso de versões inseguras do protocolo.

- 🕵️‍♂️ **Detector de Vazamento de Dados**
  - Verifica chamadas para terceiros sem criptografia.
  - Detecta envio de dados sensíveis (em construção).

- 📄 **Relatório de Compliance**
  - Gera relatório HTML com:
    - Pontos de falha encontrados.
    - Sugestões de correção.
    - Pontuação e status de conformidade.
  - Disponível após a análise completa do site.

- 🎨 **Interface Web Responsiva**
  - Desenvolvida com Bootstrap 5.
  - Feedback visual amigável e leitura fácil dos resultados.

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- Flask
- BeautifulSoup
- Selenium
- requests
- Bootstrap 5 (frontend)
- PyPDF2 / ReportLab *(em breve: geração de PDF)*

## 🚀 Como Rodar Localmente

```bash
git clone https://github.com/Emersomds/gdpr_checker.git
cd gdpr_checker

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor Flask
python app.py
