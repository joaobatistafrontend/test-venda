

altura = int(input('Qual sua altura em cm?: ')) / 100  # Converter para metros
peso = float(input('Qual seu peso em kg?: '))
imc = peso / (altura * altura)  
print(f'Seu IMC corporal é: {imc:.2f}')
