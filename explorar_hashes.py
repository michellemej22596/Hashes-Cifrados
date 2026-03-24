"""
Ejercicio 1: Comparación de algoritmos de hash
MediSoft S.A. - Cifrados de Información

Este script calcula y compara hashes usando MD5, SHA-1, SHA-256 y SHA-3/256
"""

import hashlib


def calcular_hashes(texto: str) -> dict:
    """Calcula el hash de un texto usando múltiples algoritmos."""
    data = texto.encode('utf-8')

    return {
        'MD5': hashlib.md5(data).hexdigest(),
        'SHA-1': hashlib.sha1(data).hexdigest(),
        'SHA-256': hashlib.sha256(data).hexdigest(),
        'SHA-3/256': hashlib.sha3_256(data).hexdigest()
    }


def obtener_info_algoritmo(nombre: str) -> tuple:
    """Retorna (longitud_bits, longitud_hex) para cada algoritmo."""
    info = {
        'MD5': (128, 32),
        'SHA-1': (160, 40),
        'SHA-256': (256, 64),
        'SHA-3/256': (256, 64)
    }
    return info[nombre]


def contar_bits_diferentes(hash1: str, hash2: str) -> int:
    """Cuenta los bits diferentes entre dos hashes usando XOR."""
    bytes1 = bytes.fromhex(hash1)
    bytes2 = bytes.fromhex(hash2)

    bits_diferentes = 0
    for b1, b2 in zip(bytes1, bytes2):
        xor_result = b1 ^ b2
        bits_diferentes += bin(xor_result).count('1')

    return bits_diferentes


def imprimir_tabla(resultados: list):
    """Imprime una tabla comparativa de hashes."""
    print("\n" + "=" * 120)
    print(f"{'Texto':<25} {'Algoritmo':<12} {'Bits':<8} {'Hex':<6} {'Hash'}")
    print("=" * 120)

    for texto, hashes in resultados:
        for i, (algo, hash_val) in enumerate(hashes.items()):
            bits, hex_len = obtener_info_algoritmo(algo)
            texto_mostrar = texto if i == 0 else ""
            print(f"{texto_mostrar:<25} {algo:<12} {bits:<8} {hex_len:<6} {hash_val}")
        print("-" * 120)


def main():
    # Textos a analizar
    texto1 = "MediSoft-v2.1.0"
    texto2 = "medisoft-v2.1.0"

    print("=" * 60)
    print("EJERCICIO 1: COMPARACIÓN DE ALGORITMOS DE HASH")
    print("MediSoft S.A. - Verificación de Integridad")
    print("=" * 60)

    # Calcular hashes para ambos textos
    hashes1 = calcular_hashes(texto1)
    hashes2 = calcular_hashes(texto2)

  # Imprimir tabla comparativa
    imprimir_tabla([
        (texto1, hashes1),
        (texto2, hashes2)
    ])

    # Análisis de diferencias usando XOR para SHA-256
    print("\n" + "=" * 60)
    print("ANÁLISIS DE DIFERENCIAS (SHA-256)")
    print("=" * 60)

    sha256_1 = hashes1['SHA-256']
    sha256_2 = hashes2['SHA-256']

    bits_diferentes = contar_bits_diferentes(sha256_1, sha256_2)
    total_bits = 256
    porcentaje = (bits_diferentes / total_bits) * 100

    print(f"\nHash SHA-256 de '{texto1}':")
    print(f"  {sha256_1}")
    print(f"\nHash SHA-256 de '{texto2}':")
    print(f"  {sha256_2}")
    print(f"\nBits diferentes (usando XOR): {bits_diferentes} de {total_bits} ({porcentaje:.2f}%)")

    # Respuestas a las preguntas de análisis
    print("\n" + "=" * 60)
    print("RESPUESTAS A PREGUNTAS DE ANÁLISIS")
    print("=" * 60)

    print(f"""
PREGUNTA 1: ¿Cuántos bits cambiaron entre los dos hashes SHA-256?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Respuesta: {bits_diferentes} bits cambiaron de un total de 256 bits.

Esto representa aproximadamente el {porcentaje:.2f}% del hash total.

¿Qué propiedad demuestra esto?
Esta diferencia demuestra el EFECTO AVALANCHA (Avalanche Effect):
- Un cambio mínimo en la entrada (solo cambiar mayúsculas por minúsculas)
  produce un cambio drástico y aparentemente aleatorio en la salida.
- Idealmente, ~50% de los bits deberían cambiar (≈128 bits para SHA-256).
- Esto hace imposible predecir cómo cambiará el hash basándose en el cambio
  de entrada, lo cual es esencial para la seguridad criptográfica.

PREGUNTA 2: ¿Por qué MD5 es considerado inseguro para integridad de archivos?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Respuesta basada en la longitud de bits:

MD5 produce hashes de solo 128 bits, lo cual presenta varios problemas:

1. VULNERABILIDAD A COLISIONES:
   - Con 128 bits, por la paradoja del cumpleaños, se necesitan solo 2^64
     operaciones para encontrar una colisión (dos entradas diferentes con
     el mismo hash).
   - En 2004, investigadores demostraron colisiones prácticas en MD5.
   - Hoy en día, se pueden generar colisiones en segundos con hardware común.

2. ATAQUES DE PRE-IMAGEN:
   - El espacio de búsqueda de 2^128 que antes parecía seguro, ahora es
     vulnerable con técnicas criptográficas avanzadas.

3. COMPARACIÓN CON ALTERNATIVAS SEGURAS:
   - SHA-256 usa 256 bits (2^128 operaciones para colisiones)
   - SHA-3/256 también usa 256 bits con diseño más moderno
   - Esto hace que MD5 sea 2^64 veces más fácil de atacar que SHA-256.

CONCLUSIÓN: Para integridad de archivos médicos críticos como los de MediSoft,
usar MD5 permitiría a un atacante crear archivos maliciosos con el mismo hash,
comprometiendo la seguridad de los equipos de diagnóstico hospitalarios.
""")


if __name__ == "__main__":
    main()
