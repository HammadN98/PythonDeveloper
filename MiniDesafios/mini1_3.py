'''
Desafio
Paulinho tem em suas mãos um novo problema. Agora a sua professora lhe pediu que construísse um programa para verificar, à partir de dois valores muito grandes A e B, se B corresponde aos últimos dígitos de A.

Entrada
A entrada consiste de vários casos de teste. A primeira linha de entrada contém um inteiro N que indica a quantidade de casos de teste. Cada caso de teste consiste de dois valores A e B maiores que zero, cada um deles podendo ter até 1000 dígitos.

Saída
Para cada caso de entrada imprima uma mensagem indicando se o segundo valor encaixa no primeiro valor, confome exemplo abaixo.

 
Exemplo de Entrada						
4
56234523485723854755454545478690 78690  
5434554 543455
1243 1243
54 64545454545454545454545454545454554

Exemplo de Saída
encaixa
nao encaixa
encaixa
nao encaixa

'''
n = int(input ())

while n > 0:
  a, b = input().split()
  
  if a.endswith(b): 
    print("encaixa")
  else:
    print ("nao encaixa")
    
  n -=1