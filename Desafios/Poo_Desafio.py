from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod
from datetime import datetime

# 3:20
class Conta:
    def __init__(self, numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)  # retorna uma instancia de Conta

    def sacar(self, valor):
        saldo = self.saldo
        tem_saldo = valor > saldo

        if tem_saldo:
            print("Operacao falhou. Saldo INSUFICIENTE!")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado!")

        else:
            print("Operacao falhou, numero informado falhou!")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._valor += valor
            print("deposito Realizado com SUCESSO!")

        else:
            print("Operecao falhou, valor informado eh invalido ")
            return False
        return True


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):  # Tem q passar o endereco que vem de Cliente
        super().__init__(endereco)  # Tem q passar o endereco que de Cliente
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes 
            if transacao["tipo"] == Saque.__name__]
            )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Valor de saque passou dos limites e operacao falhou!")

        elif excedeu_saques:
            print("Numero maximo de saques exedido!")
            
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
        Agencia: {self.agencia}
        C/c: {self.numero}
        Titular: {self.cliente.nome}
        """
    

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacoes(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor" : transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%s"),
            }
        )        

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
     def __init__(self, valor):
        self._valor = valor

     @property
     def valor(self):
        return self._valor
    
     def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# acabou video 1


def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        
        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado!")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente nao possui conta! ")
        return
    # FIXME: NAo permite cliente escolher a conta
    return cliente.contas[0]

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado! ")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado! ")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("____________________ EXTRATO ____________________")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Nao foram realizados operacoes na conta"
    else:
        for transacao in transacoes:
            extrato += f"{transacao["tipo"]}: R$ {transacao["valor"]:.2f}"

    print(extrato)
    print(f"Saldo: R$ {conta.saldo:.2f}")
    print("_________________________________________________")

def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("ja existe cliente com esse CPF")
        return
    
    nome = input("Informe o Nome Completo: ")
    data_nascimento = input("Digite a Data de Nasciemnto")
    endereco = ("Infomre endereco")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    print("Cliente criado com sucesso")
#

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado! ")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print(" Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas: 
        print("=" * 100)
        print(conta)


def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """
    return input(menu)