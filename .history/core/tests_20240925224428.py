
def calcular_area_quadrado(lado):
    """Calcula a área de um quadrado."""
    return lado ** 2

def calcular_area_retangulo(base, altura):
    """Calcula a área de um retângulo."""
    return base * altura

    lado_quadrado = 4
    area_quadrado = calcular_area_quadrado(lado_quadrado)
    print(f"A área do quadrado com lado {lado_quadrado} é: {area_quadrado}")

    base_retangulo = 5
    altura_retangulo = 3
    area_retangulo = calcular_area_retangulo(base_retangulo, altura_retangulo)
    print(f"A área do retângulo com base {base_retangulo} e altura {altura_retangulo} é: {area_retangulo}")
