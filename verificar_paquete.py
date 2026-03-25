"""
Ejercicio 3 (Parte 2): Verificación de integridad de paquetes
MediSoft S.A. - Cifrados de Información

Este script simula al administrador TI del hospital.
Verifica que los archivos descargados coinciden con el manifiesto SHA256SUMS.txt
"""

import hashlib
import os
import sys


def calcular_sha256_archivo(filepath: str) -> str:
    """Calcula el hash SHA-256 de un archivo."""
    sha256_hash = hashlib.sha256()

    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def leer_manifiesto(manifiesto_path: str) -> dict:
    """
    Lee el archivo de manifiesto y retorna un diccionario.

    Formato esperado: <HASH>  <nombre_archivo>
    """
    hashes = {}

    with open(manifiesto_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # El formato estándar usa dos espacios entre hash y nombre
            parts = line.split('  ', 1)
            if len(parts) != 2:
                # Intentar con un espacio
                parts = line.split(' ', 1)

            if len(parts) == 2:
                hash_value, filename = parts
                hashes[filename.strip()] = hash_value.strip().lower()
            else:
                print(f"  ⚠️  Línea {line_num} mal formateada: {line}")

    return hashes


def verificar_paquete(manifiesto_path: str = "SHA256SUMS.txt", directorio: str = "paquete_medisoft"):
    """
    Verifica la integridad de los archivos contra el manifiesto.

    Args:
        manifiesto_path: Ruta al archivo de manifiesto
        directorio: Directorio donde buscar los archivos
    """
    print("=" * 70)
    print("VERIFICADOR DE INTEGRIDAD - Hospital IT Admin")
    print("=" * 70)

    # Verificar que existe el manifiesto
    if not os.path.exists(manifiesto_path):
        print(f"\n✗ Error: No se encontró el manifiesto: {manifiesto_path}")
        print("  Ejecute primero: python generar_manifiesto.py")
        return False

    print(f"\nManifiesto: {manifiesto_path}")
    print(f"Directorio: {directorio}")

    # Leer el manifiesto
    hashes_esperados = leer_manifiesto(manifiesto_path)

    if not hashes_esperados:
        print("\n✗ Error: El manifiesto está vacío o mal formateado")
        return False

    print(f"Archivos a verificar: {len(hashes_esperados)}")
    print("\n" + "-" * 70)
    print("RESULTADOS DE VERIFICACIÓN")
    print("-" * 70)

    correctos = []
    incorrectos = []
    no_encontrados = []

    for filename, hash_esperado in hashes_esperados.items():
        # Buscar el archivo
        filepath = os.path.join(directorio, filename)

        # Si no está en el directorio, buscar en el directorio actual
        if not os.path.exists(filepath):
            filepath = filename

        if not os.path.exists(filepath):
            no_encontrados.append(filename)
            print(f"  ⚠️  NO ENCONTRADO: {filename}")
            continue

        # Calcular el hash actual
        hash_actual = calcular_sha256_archivo(filepath)

        if hash_actual == hash_esperado:
            correctos.append(filename)
            print(f"  ✓  OK: {filename}")
        else:
            incorrectos.append({
                'archivo': filename,
                'esperado': hash_esperado,
                'actual': hash_actual
            })
            print(f"  ✗  FALLIDO: {filename}")
            print(f"      Esperado: {hash_esperado}")
            print(f"      Actual:   {hash_actual}")

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 70)

    total = len(hashes_esperados)
    print(f"\n  Total de archivos en manifiesto: {total}")
    print(f"  ✓ Verificados correctamente:     {len(correctos)}")
    print(f"  ✗ Verificación fallida:          {len(incorrectos)}")
    print(f"  ⚠️  No encontrados:               {len(no_encontrados)}")

    if incorrectos:
        print("\n" + "-" * 70)
        print("⚠️  ALERTA DE SEGURIDAD: ARCHIVOS MODIFICADOS DETECTADOS")
        print("-" * 70)
        for item in incorrectos:
            print(f"\n  Archivo: {item['archivo']}")
            print(f"  Hash esperado: {item['esperado']}")
            print(f"  Hash actual:   {item['actual']}")
        print("\n  ACCIÓN REQUERIDA:")
        print("  - NO instale este paquete")
        print("  - Descargue nuevamente desde el servidor oficial de MediSoft")
        print("  - Reporte este incidente al equipo de seguridad")
        return False

    if no_encontrados:
        print("\n  ⚠️  Advertencia: Algunos archivos no fueron encontrados")
        print("      Esto podría indicar un paquete incompleto")

    if len(correctos) == total:
        print("\n  ✓ VERIFICACIÓN EXITOSA")
        print("    Todos los archivos coinciden con el manifiesto de MediSoft")
        print("    El paquete es seguro para instalar")
        return True

    return False


def modificar_archivo_prueba(directorio: str = "paquete_medisoft"):
    """Modifica un byte de un archivo para demostrar la detección."""
    archivo_objetivo = os.path.join(directorio, "config.xml")

    if not os.path.exists(archivo_objetivo):
        print(f"No se encontró el archivo de prueba: {archivo_objetivo}")
        return False

    print("\n" + "=" * 70)
    print("SIMULACIÓN DE ATAQUE: Modificando archivo")
    print("=" * 70)

    # Leer contenido original
    with open(archivo_objetivo, 'rb') as f:
        contenido = bytearray(f.read())

    print(f"\nArchivo objetivo: {archivo_objetivo}")
    print(f"Tamaño: {len(contenido)} bytes")

    # Modificar un byte (cambiar 'true' por 'True' en el XML)
    contenido_str = contenido.decode('utf-8')
    if 'true' in contenido_str:
        contenido_modificado = contenido_str.replace('true', 'True', 1)
        print("Modificación: Cambiar 'true' por 'True'")
    else:
        # Modificar el primer byte alfabético
        for i, byte in enumerate(contenido):
            if 65 <= byte <= 90 or 97 <= byte <= 122:  # A-Z o a-z
                contenido[i] = byte ^ 0x20  # Cambiar mayúscula/minúscula
                print(f"Modificación: Byte {i} cambiado de {chr(byte)} a {chr(contenido[i])}")
                contenido_modificado = contenido.decode('utf-8', errors='replace')
                break
        else:
            contenido[0] = (contenido[0] + 1) % 256
            print(f"Modificación: Primer byte incrementado")
            contenido_modificado = contenido.decode('utf-8', errors='replace')

    # Escribir archivo modificado
    with open(archivo_objetivo, 'w') as f:
        f.write(contenido_modificado)

    print("\n✓ Archivo modificado exitosamente")
    print("  Ahora ejecute la verificación para detectar el cambio")

    return True


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--modificar":
        # Modo de prueba: modificar un archivo
        modificar_archivo_prueba()
        print("\n")

    resultado = verificar_paquete()

    if not resultado:
        print("\n" + "=" * 70)
        print("DEMOSTRACIÓN: Para probar la detección de modificaciones")
        print("=" * 70)
        print("""
Ejecute el siguiente comando para modificar un archivo y luego verificar:

  python verificar_paquete.py --modificar
  python verificar_paquete.py

O manualmente:
1. Abra cualquier archivo en paquete_medisoft/ con un editor
2. Cambie un solo carácter
3. Guarde el archivo
4. Ejecute: python verificar_paquete.py
""")


if __name__ == "__main__":
    main()
