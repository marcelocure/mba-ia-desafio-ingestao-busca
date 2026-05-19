from search import search_prompt


def main():
    reply = search_prompt()

    if not reply:
        print("## Não foi possível iniciar o chat. Verifique os logs de inicialização.")
        return

    print("## Faça sua pergunta:\n")

    while True:
        try:
            pergunta = input("## PERGUNTA: ").strip()
        except (EOFError, KeyboardInterrupt) as e:
            print(f"Erro ao ler a pergunta: {e}")
            break

        if not pergunta:
            break

        resposta = reply(pergunta)
        print(f"##RESPOSTA: {resposta}\n")


if __name__ == "__main__":
    main()
