"""
Ejercicio 2: Verificación de contraseñas en Have I Been Pwned
MediSoft S.A. - Cifrados de Información

Este script verifica contraseñas comunes contra la API de HIBP usando k-Anonymity.
IMPORTANTE: La API de HIBP usa SHA-1, no SHA-256.
"""

import hashlib
import requests


def calcular_sha1(texto: str) -> str:
    """Calcula el hash SHA-1 de un texto (requerido por HIBP)."""
    return hashlib.sha1(texto.encode('utf-8')).hexdigest().upper()


def calcular_sha256(texto: str) -> str:
    """Calcula el hash SHA-256 de un texto."""
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()


def verificar_en_hibp(password: str) -> int:
    """
    Verifica si una contraseña ha sido expuesta en filtraciones usando HIBP.

    Usa el modelo k-Anonymity:
    - Solo envía los primeros 5 caracteres del hash SHA-1
    - Recibe todos los sufijos que coinciden
    - El hash completo nunca sale de la máquina

    Retorna: número de veces que aparece en filtraciones (0 si no aparece)
    """
    # HIBP usa SHA-1 para su API
    sha1_hash = calcular_sha1(password)

    # Dividir el hash: primeros 5 caracteres y el resto
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    # Consultar la API de HIBP
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        response = requests.get(url, headers={'User-Agent': 'MediSoft-Security-Check'})
        response.raise_for_status()

        # Buscar el sufijo en la respuesta
        # El formato es: SUFIJO:CONTEO (uno por línea)
        for line in response.text.splitlines():
            parts = line.split(':')
            if len(parts) == 2:
                hash_suffix, count = parts
                if hash_suffix.upper() == suffix:
                    return int(count)

        return 0

    except requests.RequestException as e:
        print(f"  Error al consultar HIBP: {e}")
        return -1


def main():
    print("=" * 80)
    print("EJERCICIO 2: VERIFICACIÓN DE CONTRASEÑAS EN HAVE I BEEN PWNED")
    print("MediSoft S.A. - Seguridad de Credenciales")
    print("=" * 80)

    # Lista de contraseñas comunes a verificar
    passwords = ["admin", "123456", "hospital", "medisoft2024"]

    print("\n" + "-" * 80)
    print(f"{'Contraseña':<20} {'SHA-256 Hash':<66} {'Filtraciones'}")
    print("-" * 80)

    resultados = []

    for password in passwords:
        sha256_hash = calcular_sha256(password)
        sha1_hash = calcular_sha1(password)
        count = verificar_en_hibp(password)

        resultados.append({
            'password': password,
            'sha256': sha256_hash,
            'sha1': sha1_hash,
            'count': count
        })

        if count == -1:
            count_str = "Error"
        elif count == 0:
            count_str = "No encontrada"
        else:
            count_str = f"{count:,} veces"

        print(f"{password:<20} {sha256_hash:<66} {count_str}")

    print("-" * 80)

    # Detalles adicionales
    print("\n" + "=" * 80)
    print("DETALLES DE LA VERIFICACIÓN (k-Anonymity)")
    print("=" * 80)

    for r in resultados:
        print(f"\nContraseña: '{r['password']}'")
        print(f"  SHA-1:   {r['sha1']}")
        print(f"  SHA-256: {r['sha256']}")
        print(f"  Prefijo enviado a HIBP (SHA-1): {r['sha1'][:5]}")
        print(f"  Sufijo buscado localmente:      {r['sha1'][5:]}")
        if r['count'] > 0:
            print(f"  ⚠️  ADVERTENCIA: Esta contraseña ha sido expuesta {r['count']:,} veces")
        elif r['count'] == 0:
            print(f"  ✓  Esta contraseña no aparece en filtraciones conocidas")

    # Análisis de seguridad
    print("\n" + "=" * 80)
    print("ANÁLISIS DE SEGURIDAD")
    print("=" * 80)
    print("""
¿Por qué SHA-256 directo sobre contraseñas es inseguro?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. TABLAS RAINBOW:
   - Los hashes de contraseñas comunes ya están pre-calculados y almacenados
     en enormes bases de datos públicas.
   - Un atacante puede simplemente buscar el hash y encontrar la contraseña
     original en milisegundos.

2. VELOCIDAD DE CÁLCULO:
   - SHA-256 está diseñado para ser RÁPIDO, lo cual es malo para contraseñas.
   - Un atacante puede calcular millones de hashes por segundo con GPUs.

3. SIN SALT:
   - Dos usuarios con la misma contraseña tendrán el mismo hash.
   - Un atacante puede atacar múltiples cuentas simultáneamente.

SOLUCIÓN CORRECTA PARA ALMACENAR CONTRASEÑAS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Usar algoritmos diseñados para contraseñas: bcrypt, scrypt, o Argon2
- Estos algoritmos:
  • Son intencionalmente LENTOS (configurable)
  • Incluyen SALT automático (único por contraseña)
  • Resisten ataques con hardware especializado

Ejemplo con bcrypt:
  import bcrypt
  hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
""")


if __name__ == "__main__":
    main()
