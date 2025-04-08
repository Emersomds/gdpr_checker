# 🛡️ GDPR / LGPD Compliance Checker

Uma ferramenta web que audita sites automaticamente em busca de violações à LGPD (Brasil) e GDPR (Europa).

## 🔍 Funcionalidades

- ✅ **Scanner de Cookies e Rastreadores**
  - Detecta cookies como Google Analytics, Meta Pixel, etc.
  - Classifica por tipo: marketing, análise, funcional.

- 🕵️‍♂️ **Detector de Vazamento de Dados**
  - Verifica chamadas para terceiros sem criptografia.
  - Detecta envio de dados sensíveis.

- 📄 **Relatório de Compliance**
  - Gera relatório HTML/PDF com:
    - Pontos de falha encontrados.
    - Sugestões de correção.

- 🔐 **Verificador de SSL/TLS**
  - Avalia força da criptografia do site.
  - Identifica uso de versões inseguras do protocolo.

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- Flask
- BeautifulSoup
- requests
- PyPDF2 / ReportLab (PDF)
- Bootstrap (na interface web)

## 🚀 Como Rodar Localmente

```bash
git clone https://github.com/Emersomds/gdpr_checker.git
cd gdpr_checker
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
