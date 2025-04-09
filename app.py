import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import ssl
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urlparse
import time
from http.cookies import SimpleCookie
from datetime import datetime

app = Flask(__name__)

# 🔍 Função para detectar rastreadores por tags <script>
def escanear_rastreadores(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', src=True)

        rastreadores = []
        for script in scripts:
            src = script['src']
            if any(tracker in src for tracker in ['googletagmanager', 'google-analytics', 'facebook.net', 'fbcdn']):
                rastreadores.append(src)

        return rastreadores
    except Exception as e:
        return [f'Erro ao acessar o site: {e}']

# 🔐 Verifica conexão SSL/TLS
def verificar_ssl_tls(url):
    try:
        if not url.startswith('https'):
            url = 'https://' + url

        hostname = urlparse(url).hostname
        port = 443

        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                versao_tls = ssock.version()
                return f"✅ Conexão segura: {versao_tls}"
    except Exception as e:
        return f"❌ Erro na verificação SSL/TLS: {e}"

# 🍪 Escaneia cookies com Selenium (usando Chrome agora)
def escanear_cookies(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    if not url.startswith("http"):
        url = "https://" + url

    driver.get(url)
    time.sleep(5)

    cookies = driver.get_cookies()
    resultados = []

    for cookie in cookies:
        nome = cookie.get("name")
        dominio = cookie.get("domain")

        if 'google' in dominio or 'facebook' in dominio:
            tipo = "Marketing"
        elif 'analytics' in nome.lower():
            tipo = "Analytics"
        else:
            tipo = "Funcional"

        resultados.append({
            'nome': nome,
            'dominio': dominio,
            'tipo': tipo
        })

    driver.quit()
    return resultados

def analisar_cookies(site_url):
    cookies_detectados = []
    try:
        response = requests.get(site_url, timeout=10)
        if 'set-cookie' in response.headers:
            raw_cookies = response.headers.get('set-cookie')
            simple_cookie = SimpleCookie()
            simple_cookie.load(raw_cookies)

            for key, morsel in simple_cookie.items():
                cookie_info = {
                    'nome': key,
                    'dominio': response.url,
                    'valor': morsel.value,
                    'risco': '🔴 Alto' if 'session' in key.lower() or 'auth' in key.lower() else '🟢 Baixo'
                }
                cookies_detectados.append(cookie_info)
    except Exception as e:
        print(f"Erro ao analisar cookies com requests: {e}")
    return cookies_detectados

# 🔍 Detector de vazamentos de dados via HTTP
def detectar_vazamento_dados(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)

    if not url.startswith("http"):
        url = "https://" + url

    driver.get(url)
    time.sleep(5)

    logs = driver.get_log("performance")
    vazamentos = []

    for entry in logs:
        message = entry["message"]
        if "Network.requestWillBeSent" in message and "http://" in message:
            url_inicio = message.find("http://")
            url_fim = message.find('"', url_inicio)
            link = message[url_inicio:url_fim]
            vazamentos.append(link)

    driver.quit()
    return vazamentos

# 🌐 Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    site_url = None
    rastreadores = []
    resultado_ssl = None
    cookies = []
    cookies_requests = []

    if request.method == 'POST':
        site_url = request.form['url']
        if not site_url.startswith('http'):
            site_url = 'https://' + site_url

        rastreadores = escanear_rastreadores(site_url)
        resultado_ssl = verificar_ssl_tls(site_url)
        cookies = escanear_cookies(site_url)
        cookies_requests = analisar_cookies(site_url)

    return render_template('index.html',
                           site_url=site_url,
                           rastreadores=rastreadores,
                           resultado_ssl=resultado_ssl,
                           cookies=cookies,
                           cookies_requests=cookies_requests)



@app.route('/relatorio')
def relatorio():
    site_url = request.args.get('url')
    if not site_url:
        return "URL não informada.", 400

    # 🔎 Faça a análise novamente ou passe os dados prontos aqui
    rastreadores = escanear_rastreadores(site_url)
    resultado_ssl = verificar_ssl_tls(site_url)
    cookies_selenium = escanear_cookies(site_url)
    cookies_requests = analisar_cookies(site_url)

    # 🧠 Avaliação de conformidade (exemplo simples)
    falhas = []
    sugestoes = []
    pontuacao = 10

    if "❌" in resultado_ssl:
        falhas.append("Conexão insegura (SSL/TLS ausente ou falha).")
        sugestoes.append("Implemente HTTPS com certificado válido.")
        pontuacao -= 3

    if rastreadores:
        falhas.append("Rastreadores de terceiros detectados.")
        sugestoes.append("Configure um CMP para consentimento de rastreamento (ex: Cookiebot).")
        pontuacao -= 2

    if not cookies_selenium and not cookies_requests:
        falhas.append("Nenhum cookie identificado – pode haver bloqueio ou carregamento tardio.")
        sugestoes.append("Verifique se cookies estão sendo declarados e carregados corretamente.")
        pontuacao -= 1

    for cookie in cookies_requests:
        if '🔴' in cookie.get('risco', ''):
            falhas.append(f"Cookie de risco alto detectado: {cookie['nome']}")
            sugestoes.append("Evite cookies de sessão sem consentimento explícito.")
            pontuacao -= 1

    status = "Conforme" if pontuacao >= 8 else "Parcialmente Conforme" if pontuacao >= 5 else "Não Conforme"

    return render_template("relatorio_compliance.html",
                           site_url=site_url,
                           data_analise=datetime.now().strftime("%d/%m/%Y %H:%M"),
                           status=status,
                           pontuacao=pontuacao,
                           falhas=falhas,
                           sugestoes=sugestoes)


if __name__ == '__main__':
    app.run(debug=True)
