from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def get_saldo(self):
        return self._saldo   

    @property
    def get_numero(self):
        return self._numero

    @property
    def get_agencia(self):
        return self._agencia

    @property
    def get_cliente(self):
        return self._cliente

    @property
    def get_historico(self):
        return self._historico
     
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        saldo = self.get_saldo

        if valor > saldo:
            print("\nSaldo insuficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\nValor inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\nValor inválido.")
            return False

        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def get_limite(self):
        return self._limite
    
    def get_limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.get_historico.get_transacoes if transacao["tipo"] == Saque.__name__]
        )

        if valor > self.get_limite():
            print("\nSem limite suficiente.")

        elif numero_saques >= self.get_limite_saques():
            print("\nNúmero máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.get_agencia}
            C/C:\t{self.get_numero}
            Titular:\t{self.get_cliente.get_nome()}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def get_transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.get_valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def get_valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def get_valor(self):
        return self._valor

    def registrar(self, conta):
        deposito = conta.depositar(self.get_valor)
        if deposito:
            conta.get_historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def get_valor(self):
        return self._valor

    def registrar(self, conta):
        saque = conta.sacar(self.get_valor)
        if saque:
            conta.get_historico.adicionar_transacao(self)
             

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def get_endereco(self):
        return self._endereco
    
    def get_contas(self):
        return self._contas
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adiconar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    def get_cpf(self):
        return self._cpf

    def get_nome(self):
        return self._nome
    
    def get_data_nascimento(self):
        return self._data_nascimento
    
def menu():
    menu = """\n
    ================ MENU ================
    [1]\tCadastrar novo Cliente
    [2]\tCadastrar nova Conta
    [3]\tDepositar
    [4]\tSacar
    [5]\tExtrato
    [6]\tMostar contas
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))
    
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            endereco = input("Informe o endereço do cliente: ")
            cpf = input("Informe o CPF do cliente: ")
            nome = input("Informe o nome do cliente: ")
            data_nascimento = input("Informe a data de nascimento do cliente (dd-mm-aaaa): ")
            cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
            clientes.append(cliente)

        elif opcao == "2":
            if not clientes:
                print("Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
                continue
            cliente = None
            while not cliente:
                cpf = input("Informe o CPF do cliente para o qual a conta será criada: ")
                for c in clientes:
                    if c.get_cpf() == cpf:
                        cliente = c
                        break
                if not cliente:
                    print("Cliente não encontrado. Tente novamente.")
            numero = input("Informe o número da conta: ")
            conta = ContaCorrente.nova_conta(cliente, numero)
            cliente.adiconar_conta(conta)
            contas.append(conta)

        elif opcao == "3":
            if not contas:
                print("Nenhuma conta cadastrada. Cadastre uma conta primeiro.")
                continue
            conta = None
            while not conta:
                numero = input("Informe o número da conta para a qual o depósito será realizado: ")
                for c in contas:
                    if c.get_numero == numero:
                        conta = c
                        break
                if not conta:
                    print("Conta não encontrada. Tente novamente.")
            valor = float(input("Informe o valor do depósito: "))
            deposito = Deposito(valor)
            conta.get_cliente.realizar_transacao(conta, deposito)

        elif opcao == "4":
            if not contas:
                print("Nenhuma conta cadastrada. Cadastre uma conta primeiro.")
                continue
            conta = None
            while not conta:
                numero = input("Informe o número da conta da qual o saque será realizado: ")
                for c in contas:
                    if c.get_numero == numero:
                        conta = c
                        break
                if not conta:
                    print("Conta não encontrada. Tente novamente.")
            valor = float(input("Informe o valor do saque: "))
            saque = Saque(valor)
            conta.get_cliente.realizar_transacao(conta, saque)

        elif opcao == "5":
            if not contas:
                print("Nenhuma conta cadastrada. Cadastre uma conta primeiro.")
                continue
            conta = None
            while not conta:
                numero = input("Informe o número da conta para a qual o extrato será exibido: ")
                for c in contas:
                    if c.get_numero == numero:
                        conta = c
                        break
                if not conta:
                    print("Conta não encontrada. Tente novamente.")
            print(conta)
            for transacao in conta.get_historico.get_transacoes:
                print(transacao)
            print(f"\nSaldo atual da conta: {conta.get_saldo}")

        elif opcao == "6":
            for conta in contas:
                print(conta)

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")


main()
