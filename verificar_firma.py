"""
Ejercicio 5: Verificación de firma digital
MediSoft S.A. - Cifrados de Información

Este script verifica la autenticidad del manifiesto usando la firma digital
y la clave pública de MediSoft.
"""

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import os
import sys


def verificar_firma(manifiesto_path: str = "SHA256SUMS.txt",
                    firma_path: str = "SHA256SUMS.sig",
                    clave_publica_path: str = "medisoft_pub.pem") -> bool:
    """
    Verifica la firma digital del manifiesto.

    Args:
        manifiesto_path: Ruta al archivo de manifiesto
        firma_path: Ruta al archivo de firma
        clave_publica_path: Ruta a la clave pública

    Returns:
        True si la firma es válida, False en caso contrario
    """
    print("=" * 70)
    print("VERIFICADOR DE FIRMA DIGITAL - Hospital IT Admin")
    print("=" * 70)

    # Verificar que existen todos los archivos necesarios
    archivos_requeridos = [
        (manifiesto_path, "Manifiesto de hashes"),
        (firma_path, "Firma digital"),
        (clave_publica_path, "Clave pública de MediSoft")
    ]

    print("\nVerificando archivos requeridos:")
    for filepath, descripcion in archivos_requeridos:
        if os.path.exists(filepath):
            print(f"  ✓ {descripcion}: {filepath}")
        else:
            print(f"  ✗ {descripcion}: {filepath} - NO ENCONTRADO")
            print(f"\n    Error: Falta el archivo {filepath}")
            print("    Asegúrese de tener todos los archivos del paquete de MediSoft")
            return False

    # Cargar la clave pública
    print("\n" + "-" * 70)
    print("CARGANDO CLAVE PÚBLICA")
    print("-" * 70)

    with open(clave_publica_path, 'rb') as f:
        clave_publica = RSA.import_key(f.read())

    print(f"Clave pública cargada exitosamente")
    print(f"  Tamaño: {clave_publica.size_in_bits()} bits")
    print(f"  Exponente (e): {clave_publica.e}")

    # Leer el manifiesto
    print("\n" + "-" * 70)
    print("LEYENDO MANIFIESTO")
    print("-" * 70)

    with open(manifiesto_path, 'rb') as f:
        contenido_manifiesto = f.read()

    print(f"Manifiesto: {manifiesto_path}")
    print(f"Tamaño: {len(contenido_manifiesto)} bytes")

    # Calcular el hash del manifiesto
    hash_manifiesto = SHA256.new(contenido_manifiesto)
    print(f"SHA-256: {hash_manifiesto.hexdigest()}")

    # Leer la firma
    print("\n" + "-" * 70)
    print("LEYENDO FIRMA")
    print("-" * 70)

    with open(firma_path, 'rb') as f:
        firma = f.read()

    print(f"Firma: {firma_path}")
    print(f"Tamaño: {len(firma)} bytes")

    # Verificar la firma
    print("\n" + "-" * 70)
    print("VERIFICANDO FIRMA")
    print("-" * 70)

    try:
        pkcs1_15.new(clave_publica).verify(hash_manifiesto, firma)
        print("\n" + "=" * 70)
        print("✓ FIRMA VÁLIDA")
        print("=" * 70)
        print("""
La firma digital es VÁLIDA. Esto garantiza que:

1. AUTENTICIDAD: El manifiesto fue creado por MediSoft S.A.
   (Solo quien posee la clave privada puede generar esta firma)

2. INTEGRIDAD: El manifiesto NO ha sido modificado desde que fue firmado
   (Cualquier cambio invalidaría la firma)

El manifiesto es auténtico y confiable.
Puede proceder a verificar los archivos del paquete.
""")
        return True

    except (ValueError, TypeError) as e:
        print("\n" + "=" * 70)
        print("✗ FIRMA INVÁLIDA")
        print("=" * 70)
        print(f"""
¡ALERTA DE SEGURIDAD!

La firma digital NO es válida. Esto puede significar:

1. El manifiesto fue MODIFICADO después de ser firmado
   (Un atacante pudo haber alterado los hashes)

2. La firma fue FALSIFICADA o CORROMPIDA
   (El archivo de firma no corresponde al manifiesto)

3. Se está usando una clave pública INCORRECTA
   (Verifique que medisoft_pub.pem es la clave oficial de MediSoft)

ACCIÓN REQUERIDA:
- NO confíe en el contenido del manifiesto
- NO instale el paquete de software
- Contacte a MediSoft para obtener archivos legítimos
- Reporte este incidente al equipo de seguridad

Error técnico: {e}
""")
        return False


def modificar_manifiesto_prueba(manifiesto_path: str = "SHA256SUMS.txt"):
    """Modifica un carácter del manifiesto para demostrar la detección."""
    if not os.path.exists(manifiesto_path):
        print(f"No se encontró el manifiesto: {manifiesto_path}")
        return False

    print("\n" + "=" * 70)
    print("SIMULACIÓN DE ATAQUE: Modificando manifiesto")
    print("=" * 70)

    with open(manifiesto_path, 'r') as f:
        contenido = f.read()

    print(f"\nContenido original (primeros 100 caracteres):")
    print(f"  {contenido[:100]}...")

    # Cambiar un carácter del hash (ej: 'a' -> 'b')
    contenido_modificado = list(contenido)
    for i, char in enumerate(contenido_modificado):
        if char.isalpha() and char.lower() in 'abcdef':
            original = char
            contenido_modificado[i] = chr((ord(char.lower()) - ord('a') + 1) % 6 + ord('a'))
            if original.isupper():
                contenido_modificado[i] = contenido_modificado[i].upper()
            print(f"\nModificación: Posición {i}, '{original}' -> '{contenido_modificado[i]}'")
            break

    contenido_modificado = ''.join(contenido_modificado)

    with open(manifiesto_path, 'w') as f:
        f.write(contenido_modificado)

    print(f"\nContenido modificado (primeros 100 caracteres):")
    print(f"  {contenido_modificado[:100]}...")

    print("\n✓ Manifiesto modificado. Ahora ejecute la verificación.")
    return True


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--modificar":
            modificar_manifiesto_prueba()
            print("\n")

    firma_valida = verificar_firma()

    if firma_valida:
        print("\n" + "-" * 70)
        print("SIGUIENTE PASO")
        print("-" * 70)
        print("""
Ahora que ha verificado la autenticidad del manifiesto, puede verificar
la integridad de los archivos del paquete:

  python verificar_paquete.py
""")

    print("\n" + "=" * 70)
    print("DEMOSTRACIÓN: Prueba de detección de alteraciones")
    print("=" * 70)
    print("""
Para demostrar que la firma detecta cualquier modificación:

1. Modificar el manifiesto:
   python verificar_firma.py --modificar
   python verificar_firma.py

2. O manualmente:
   - Abra SHA256SUMS.txt con un editor
   - Cambie un solo carácter de cualquier hash
   - Guarde el archivo
   - Ejecute: python verificar_firma.py
""")

    # Respuesta a la pregunta del ejercicio
    print("\n" + "=" * 70)
    print("RESPUESTA A LA PREGUNTA DE ANÁLISIS")
    print("=" * 70)
    print("""
PREGUNTA: ¿Por qué la firma es válida después de modificar un archivo de datos?
          ¿Qué sucede al ejecutar verificar_paquete.py?

RESPUESTA:
━━━━━━━━━━

La firma digital en SHA256SUMS.sig firma únicamente el CONTENIDO del archivo
SHA256SUMS.txt (el manifiesto de hashes), NO los archivos de datos directamente.

FLUJO DE VERIFICACIÓN DE DOS CAPAS:

┌─────────────────────────────────────────────────────────────────────┐
│  CAPA 1: Autenticidad (verificar_firma.py)                         │
│  ─────────────────────────────────────────                         │
│  Verifica: ¿El manifiesto SHA256SUMS.txt es auténtico?             │
│  Método:   Validar firma RSA con clave pública                     │
│  Resultado: Si el MANIFIESTO no fue alterado → Firma VÁLIDA        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CAPA 2: Integridad (verificar_paquete.py)                         │
│  ─────────────────────────────────────────                         │
│  Verifica: ¿Los archivos coinciden con los hashes del manifiesto?  │
│  Método:   Recalcular SHA-256 de cada archivo y comparar           │
│  Resultado: Si un ARCHIVO fue modificado → Hash NO coincide        │
└─────────────────────────────────────────────────────────────────────┘

POR LO TANTO:

1. Si modificamos un ARCHIVO DE DATOS (ej: config.xml):
   - verificar_firma.py → VÁLIDA (el manifiesto no cambió)
   - verificar_paquete.py → FALLA (el hash del archivo no coincide)

2. Si modificamos el MANIFIESTO (SHA256SUMS.txt):
   - verificar_firma.py → INVÁLIDA (detecta alteración)
   - verificar_paquete.py → Podría pasar si los hashes fueron recalculados
                           PERO la firma ya falló, así que no importa

CONCLUSIÓN:
El sistema de dos capas garantiza que un atacante no puede:
- Modificar archivos sin ser detectado (Capa 2 falla)
- Modificar el manifiesto para ocultar cambios (Capa 1 falla)

Ambas verificaciones son necesarias para seguridad completa.
""")


if __name__ == "__main__":
    main()
