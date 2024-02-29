'''Criando um sistema bancario: Fase 1'''
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
csaque = 1

while True:
	opcao = input(menu)

	if opcao == "d":
		print('depositos')
		deposito = float(input("Digite o valor a ser depositado: R$ "))
		while deposito <= 0:
			deposito = float(input("Valor insuficiente para ser depositado. Digite o valor a ser depositado: R$ "))
		saldo += deposito
		extrato += f"""     Valor depositado: R$ {deposito:.2f}\n"""
	  
	elif opcao == "s":
		print("Saque")
		saque = int(input("Digite o valor do saque: R$ "))
		if numero_saques >= LIMITE_SAQUES:
			print("Numero maximo de saques atingido")

		elif saque > saldo:
			print(f"Saldo insuficiente. Seu saldo atual e {saldo:.2f}")	

		elif saque > limite:
			print("Nao e possivel sacar mais de R$ 500.00. Recomece a transacao")
				
					
		else:
			saldo -= saque
			numero_saques = numero_saques + 1
			extrato += f"     Valor sacado: R$ {saque:.2f}\n"
			print(f"Saque {csaque} / 3 ")
			csaque = csaque + 1

	elif opcao == "e":
		print("\n")
		print("#############Extrato############\n")
	
		print("Nao foram realizadas operacoes." if not extrato else extrato)
		print(f"     Saldo: R$ {saldo:.2f}")
		print("#############Extrato############")

	elif opcao == "q":
		break

	else:
		print("Operacao invalida, por favor selecione novamnete a operacao desejada.")

