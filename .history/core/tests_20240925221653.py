from django.test import TestCase

altura = int(input('Qual sua altura em cm?: ')) / 100  # Converter para metros
peso = float(input('Qual seu peso em kg?: '))  # Usar float para permitir pesos com decimais
imc = peso / (altura * altura)  # Cálculo do IMC
print(f'Seu IMC corporal é: {imc:.2f}')  # Formatar para 2 casas decimais
