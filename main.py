import os
import time
import requests
import json

RESET = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"

USER_FILE = "user.json"
API_FILE = "api.json"

def save_user_data(username, password):
    user_data = {
        "username": username,
        "password": password
    }
    with open(USER_FILE, "w") as f:
        json.dump(user_data, f, indent=4)

def load_user_data():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return None

def save_api_data(api_key, access_token):
    api_data = {
        "api_key": api_key,
        "access_token": access_token
    }
    with open(API_FILE, "w") as f:
        json.dump(api_data, f, indent=4)

def load_api_data():
    if os.path.exists(API_FILE):
        with open(API_FILE, "r") as f:
            return json.load(f)
    return None

def verify_login(username, password):
    session = requests.Session()
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = session.get("https://www.instagram.com/")
    csrf_token = response.cookies["csrftoken"]

    data = {
        "username": username,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:&:{password}",
        "queryParams": {},
        "optIntoOneTap": "false"
    }

    login_headers = headers.copy()
    login_headers["X-CSRFToken"] = csrf_token

    login_response = session.post(login_url, data=data, headers=login_headers, cookies={"csrftoken": csrf_token})

    if login_response.status_code == 200 and login_response.json().get("authenticated"):
        return True
    return False

def show_header():
    os.system("clear")
    print(f"""
{RED}{BOLD}                                                        
          ──▄────▄▄▄▄▄▄▄────▄───
          ─▀▀▄─▄█████████▄─▄▀▀──
          ─────██─▀███▀─██──────
          ───▄─▀████▀████▀─▄────
          ─▀█────██▀█▀██────█▀──
{RESET}
------------------------------------------------
                {BOLD}OF BAN-INSTA{RESET}{CYAN}
        By sentinelzxofc  </>
---------------------------------------------------{RESET}
{RED}{BOLD}AVISO:{RESET} {YELLOW}Essa script é apenas para fins educativos.
Não me responsabilizo pelo uso antiético dela.
A conta logada nesse script corre risco de ban.{RESET}
    """)

def main_menu():
    show_header()
    print(f"""
{CYAN}[ 1 ] SPAM BAN{RESET}
{CYAN}[ 2 ] LOGIN{RESET}
{CYAN}[ 3 ] UPGRADE{RESET}
{CYAN}[ 4 ] API{RESET}

{RED}[ X ] EXIT{RESET}
    """)
    choice = input(f"{CYAN}DIGITE UMA OPÇÃO: {RESET}").strip()
    if choice == "1":
        run_menu2()
    elif choice == "2":
        login()
    elif choice == "3":
        upgrade()
    elif choice == "4":
        add_api()
    elif choice.lower() == "x":
        exit_script()
    else:
        print(f"\n{RED}Opção inválida! Voltando ao menu principal...{RESET}")
        time.sleep(2)
        main_menu()

def run_menu2():
    os.system("python3 menu2.py")

def login():
    show_header()
    username = input(f"{CYAN}Por favor, digite o nome do usuário (sem @): {RESET}").strip()
    password = input(f"{CYAN}Por favor, digite sua senha: {RESET}").strip()

    print(f"{CYAN}Verificando login...{RESET}")
    if verify_login(username, password):
        print(f"{CYAN}Acesso com sucesso!{RESET}")
        save_user_data(username, password)
        time.sleep(2)
        main_menu()
    else:
        print(f"{RED}Erro: Usuário ou senha incorretos, por favor verifique e tente novamente.{RESET}")
        time.sleep(2)
        login()

def upgrade():
    show_header()
    print(f"{CYAN}Iniciando upgrade...{RESET}")
    time.sleep(2)
    os.system("python3 upgrade.py")

def add_api():
    show_header()
    print(f"{CYAN}Por favor, insira as credenciais da sua API do Instagram:{RESET}")
    api_key = input(f"{CYAN}API Key: {RESET}").strip()
    access_token = input(f"{CYAN}Access Token: {RESET}").strip()

    save_api_data(api_key, access_token)
    print(f"{GREEN}API adicionada com sucesso!{RESET}")
    time.sleep(2)
    main_menu()

def exit_script():
    show_header()
    print(f"{RED}Saindo...{RESET}")
    time.sleep(1)
    os.system("clear")
    exit()

if __name__ == "__main__":
    main_menu()