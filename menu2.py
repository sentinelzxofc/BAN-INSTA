import os
import time
import requests
import json

RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"

USER_FILE = "user.json"
API_FILE = "api.json"

def load_user_data():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                data = json.load(f)
                if data:
                    return data
        except (json.JSONDecodeError, ValueError):
            pass
    return None

def load_api_data():
    if os.path.exists(API_FILE):
        try:
            with open(API_FILE, "r") as f:
                data = json.load(f)
                if data:
                    return data
        except (json.JSONDecodeError, ValueError):
            pass
    return None

def select_account():
    os.system("clear")
    user_data = load_user_data()

    if not user_data:
        print(f"{RED}Não há contas salvas! Por favor, adicione uma conta no arquivo {USER_FILE}.{RESET}")
        time.sleep(3)
        exit()

    print(f"{CYAN}Selecione uma conta para continuar:{RESET}")
    for idx, account in enumerate(user_data, start=1):
        print(f"{YELLOW}[ {idx} ] {account['username']}{RESET}")

    selected = input(f"{CYAN}Digite o número da conta: {RESET}").strip()
    try:
        selected = int(selected)
        if 1 <= selected <= len(user_data):
            return user_data[selected - 1]
        else:
            print(f"{RED}Opção inválida!{RESET}")
            time.sleep(2)
            return select_account()
    except ValueError:
        print(f"{RED}Opção inválida!{RESET}")
        time.sleep(2)
        return select_account()

def get_target_info(profile_link):
    if "?" in profile_link:
        profile_link = profile_link.split("?")[0]

    if not profile_link.startswith("https://www.instagram.com/"):
        return None, f"{RED}Link incorreto ou fora do formato esperado!{RESET}"

    username = profile_link.split("/")[3]

    try:
        response = requests.get(f"https://www.instagram.com/{username}/?__a=1")
        if response.status_code != 200:
            return None, f"{RED}Erro ao acessar o perfil. O perfil pode estar privado ou não existe.{RESET}"

        try:
            data = response.json()
        except json.JSONDecodeError:
            return None, f"{RED}Erro ao processar os dados do Instagram. A API pode estar fora do ar.{RESET}"

        profile = {"username": username, "link": profile_link}
        return profile, None
    except requests.exceptions.RequestException as e:
        return None, f"{RED}Erro ao se conectar ao Instagram: {str(e)}{RESET}"

def report_spam(api_data, target_username):
    url = "https://api.instagram.com/v1/media/{}/flag/"
    headers = {
        "Authorization": f"Bearer {api_data['access_token']}",
        "Content-Type": "application/json",
    }
    data = {"reason": "spam", "target_user": target_username}

    try:
        response = requests.post(url, headers=headers, json=data)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return None, str(e)

def spam_attack(account, api_data, profile):
    os.system("clear")
    print(f"""
{CYAN}--------------------- DENÚNCIA INICIADA ---------------------
{RESET}{BOLD}USUÁRIO ALVO:{RESET} @{profile['username']}
{BOLD}LINK DO PERFIL:{RESET} {profile['link']}
{CYAN}----------------------------------------------------------{RESET}

{RED}AVISO:{RESET} Este script fará uma única denúncia de spam.
{CYAN}----------------------------------------------------------{RESET}
    """)

    choice = input(f"{CYAN}CONFIRMA INICIAR A DENÚNCIA? (S/N): {RESET}").strip().lower()
    if choice == "n":
        print(f"{CYAN}Voltando ao menu principal...{RESET}")
        time.sleep(2)
        return
    elif choice == "s":
        print(f"{GREEN}Iniciando denúncia...{RESET}")
        status_code, response = report_spam(api_data, profile["username"])

        if status_code == 200:
            print(f"{GREEN}Denúncia enviada com sucesso!{RESET}")
            print(f"{CYAN}Detalhes da denúncia: {response}{RESET}")
        else:
            print(f"{RED}Falha ao enviar denúncia. Código: {status_code}, Erro: {response}{RESET}")

        input(f"{CYAN}Pressione ENTER para voltar ao menu principal.{RESET}")
    else:
        print(f"{RED}Opção inválida! Voltando ao menu principal.{RESET}")
        time.sleep(2)

def spam_ban():
    os.system("clear")
    account = select_account()
    api_data = load_api_data()

    if not api_data:
        print(f"{RED}Não foi possível carregar a chave da API! Verifique o arquivo {API_FILE}.{RESET}")
        time.sleep(2)
        return

    profile_link = input(f"{CYAN}Por favor, envie o link do alvo de perfil: {RESET}").strip()
    profile, error = get_target_info(profile_link)
    if error:
        print(error)
        time.sleep(2)
        return

    spam_attack(account, api_data, profile)

def menu2():
    os.system("clear")
    print(f"""
{CYAN}------------------------------------------------
              MENU DENÚNCIA{RESET}
------------------------------------------------{RESET}
{GREEN}[ 1 ] SELECIONAR CONTA E INICIAR DENÚNCIA{RESET}
{RED}[ X ] VOLTAR AO MENU PRINCIPAL{RESET}
    """)
    choice = input(f"{CYAN}DIGITE SUA OPÇÃO: {RESET}").strip()
    if choice == "1":
        spam_ban()
    elif choice.lower() == "x":
        print(f"{CYAN}Voltando ao menu principal...{RESET}")
        time.sleep(2)
        os.system("python3 main.py")
        exit()
    else:
        print(f"{RED}Opção inválida! Voltando ao menu secundário.{RESET}")
        time.sleep(2)
        menu2()

if __name__ == "__main__":
    menu2()