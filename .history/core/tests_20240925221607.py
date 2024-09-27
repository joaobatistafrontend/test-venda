from django.test import TestCase

altura = int(input('qual sua altura?: '))
peso = int(input('qual seu peso?: '))
imc = peso / (altura*altura)
print(f'seu imc corporal é: {imc}')