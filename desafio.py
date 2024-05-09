menu = """\n
================ MENU ================
[1]\tDepositar
[2]\tSacar
[3]\tExtrato
[0]\tSair
=> """
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "1":
       print("================ DEPOSITAR ================")
       valor = float(input("Digite o valor a ser depositado: "))
       if valor <= 0:
           print("Digite um valor positivo")
       else:
           saldo += valor
           extrato += f"Depósito: R$ {valor:.2f}\n"
           print("Depósito realizado com sucesso!")    
    elif opcao == "2":
        print("================ SACAR ================")
        valor = float(input("Digite o valor a ser sacado: "))
        if numero_saques >= LIMITE_SAQUES or valor > 500:
            print("Não é possível realizar o saque")
        elif valor > saldo:
            print("Saldo insuficiente")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("Saque realizado com sucesso!")       
    elif opcao == "3":
        print("================ EXTRATO ================")
        print(extrato)
        print(f"Saldo: R$ {saldo:.2f}")
    elif opcao == "0":
        break
    else:
      print("Operação inválida, por favor selecione novamente a operação desejada.")
