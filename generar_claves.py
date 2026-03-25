"""
Ejercicio 4 (Parte 1): Generación de claves RSA
MediSoft S.A. - Cifrados de Información

Este script genera un par de claves RSA de 2048 bits para firmar
digitalmente el manifiesto de integridad.
"""

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import os


def generar_claves_rsa(bits: int = 2048):
    """
    Genera un par de claves RSA y las guarda en archivos PEM.

    Args:
        bits: Tamaño de la clave en bits (default: 2048)
    """
    print("=" * 70)
    print("GENERADOR DE CLAVES RSA - MediSoft S.A.")
    print("=" * 70)

    print(f"\nGenerando par de claves RSA de {bits} bits...")
    print("(Esto puede tomar unos segundos)\n")

    # Generar el par de claves
    key = RSA.generate(bits)

    # Exportar clave privada
    private_key_pem = key.export_key()
    private_key_file = "medisoft_priv.pem"

    with open(private_key_file, 'wb') as f:
        f.write(private_key_pem)

    print(f"✓ Clave PRIVADA guardada en: {private_key_file}")
    print("  ⚠️  ADVERTENCIA: ¡NO COMPARTA ESTE ARCHIVO!")
    print("  Esta clave debe mantenerse segura y confidencial.")

    # Exportar clave pública
    public_key_pem = key.publickey().export_key()
    public_key_file = "medisoft_pub.pem"

    with open(public_key_file, 'wb') as f:
        f.write(public_key_pem)

    print(f"\n✓ Clave PÚBLICA guardada en: {public_key_file}")
    print("  Esta clave puede compartirse con los hospitales.")

    # Mostrar información de las claves
    print("\n" + "-" * 70)
    print("INFORMACIÓN DE LAS CLAVES GENERADAS")
    print("-" * 70)

    print(f"\nTamaño de clave: {bits} bits")
    print(f"Módulo (n): {key.n.bit_length()} bits")
    print(f"Exponente público (e): {key.e}")

    # Mostrar primeros/últimos caracteres de cada clave
    print("\n" + "-" * 70)
    print("CLAVE PÚBLICA (medisoft_pub.pem):")
    print("-" * 70)
    print(public_key_pem.decode())

    print("\n" + "-" * 70)
    print("CLAVE PRIVADA (medisoft_priv.pem) - VISTA PARCIAL:")
    print("-" * 70)
    private_lines = private_key_pem.decode().split('\n')
    print(private_lines[0])  # -----BEGIN RSA PRIVATE KEY-----
    print(private_lines[1][:40] + "..." + " [CONTENIDO OCULTO POR SEGURIDAD]")
    print("...")
    print(private_lines[-2][:40] + "..." if len(private_lines[-2]) > 40 else private_lines[-2])
    print(private_lines[-1])  # -----END RSA PRIVATE KEY-----

    return key


def firmar_manifiesto(manifiesto_path: str = "SHA256SUMS.txt", 
                      clave_privada_path: str = "medisoft_priv.pem",
                      firma_path: str = "SHA256SUMS.sig"):
    """
    Firma digitalmente el manifiesto usando la clave privada RSA.

    Args:
        manifiesto_path: Ruta al archivo de manifiesto
        clave_privada_path: Ruta a la clave privada PEM
        firma_path: Ruta donde guardar la firma
    """
    print("\n" + "=" * 70)
    print("FIRMA DIGITAL DEL MANIFIESTO")
    print("=" * 70)

    # Verificar que existen los archivos necesarios
    if not os.path.exists(manifiesto_path):
        print(f"\n✗ Error: No se encontró el manifiesto: {manifiesto_path}")
        print("  Ejecute primero: python generar_manifiesto.py")
        return False

    if not os.path.exists(clave_privada_path):
        print(f"\n✗ Error: No se encontró la clave privada: {clave_privada_path}")
        print("  Las claves se generarán automáticamente...")
        generar_claves_rsa()

    # Leer el contenido del manifiesto
    with open(manifiesto_path, 'rb') as f:
        contenido_manifiesto = f.read()

    print(f"\nManifiesto a firmar: {manifiesto_path}")
    print(f"Tamaño: {len(contenido_manifiesto)} bytes")

    # Calcular el hash SHA-256 del manifiesto
    hash_manifiesto = SHA256.new(contenido_manifiesto)
    print(f"SHA-256 del manifiesto: {hash_manifiesto.hexdigest()}")

    # Cargar la clave privada
    with open(clave_privada_path, 'rb') as f:
        clave_privada = RSA.import_key(f.read())

    print(f"\nClave privada cargada: {clave_privada_path}")

    # Firmar usando PKCS#1 v1.5
    print("Esquema de firma: PKCS#1 v1.5")

    firma = pkcs1_15.new(clave_privada).sign(hash_manifiesto)

    # Guardar la firma
    with open(firma_path, 'wb') as f:
        f.write(firma)

    print(f"\n✓ Firma guardada en: {firma_path}")
    print(f"  Tamaño de firma: {len(firma)} bytes ({len(firma) * 8} bits)")

    # Mostrar firma en hexadecimal (primeros y últimos bytes)
    firma_hex = firma.hex()
    print(f"\nFirma (hex):")
    print(f"  {firma_hex[:64]}...")
    print(f"  ...{firma_hex[-64:]}")

    return True


def main():
    # Paso 1: Generar las claves RSA
    generar_claves_rsa(2048)

    # Paso 2: Firmar el manifiesto (si existe)
    firmar_manifiesto()

    print("\n" + "=" * 70)
    print("SIGUIENTE PASO")
    print("=" * 70)
    print("""
Los hospitales ahora pueden verificar:
1. La integridad de los archivos (usando SHA256SUMS.txt)
2. La autenticidad del manifiesto (usando SHA256SUMS.sig y medisoft_pub.pem)

Para verificar la firma, ejecute:
  python verificar_firma.py

Archivos a distribuir a los hospitales:
  - Paquete de software (carpeta paquete_medisoft/)
  - SHA256SUMS.txt (manifiesto de hashes)
  - SHA256SUMS.sig (firma digital del manifiesto)
  - medisoft_pub.pem (clave pública para verificar)

Archivo que NUNCA debe compartirse:
  - medisoft_priv.pem (clave privada de MediSoft)
""")


if __name__ == "__main__":
    main()
