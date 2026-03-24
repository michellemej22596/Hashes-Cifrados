"""
Ejercicio 3 (Parte 1): Generación de manifiesto de integridad
MediSoft S.A. - Cifrados de Información

Este script simula el rol de MediSoft al publicar un nuevo release.
Genera un archivo SHA256SUMS.txt con los hashes de los archivos del paquete.
"""

import hashlib
import os
import sys
from datetime import datetime


def calcular_sha256_archivo(filepath: str) -> str:
    """Calcula el hash SHA-256 de un archivo."""
    sha256_hash = hashlib.sha256()

    with open(filepath, 'rb') as f:
        # Leer en bloques para archivos grandes
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def generar_manifiesto(archivos: list, output_file: str = "SHA256SUMS.txt"):
    """
    Genera un manifiesto de hashes SHA-256 para una lista de archivos.

    Args:
        archivos: Lista de rutas de archivos
        output_file: Nombre del archivo de manifiesto (default: SHA256SUMS.txt)
    """
    print("=" * 70)
    print("GENERADOR DE MANIFIESTO DE INTEGRIDAD - MediSoft S.A.")
    print("=" * 70)
    print(f"\nFecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Archivo de manifiesto: {output_file}")
    print(f"Archivos a procesar: {len(archivos)}")
    print("\n" + "-" * 70)

    resultados = []
    errores = []

    for filepath in archivos:
        if not os.path.exists(filepath):
            errores.append(f"  ✗ Archivo no encontrado: {filepath}")
            continue

        if os.path.isdir(filepath):
            errores.append(f"  ✗ Es un directorio, no un archivo: {filepath}")
            continue

        try:
            hash_value = calcular_sha256_archivo(filepath)
            filename = os.path.basename(filepath)
            resultados.append((hash_value, filename, filepath))
            print(f"  ✓ {filename}")
            print(f"    SHA-256: {hash_value}")
        except Exception as e:
            errores.append(f"  ✗ Error procesando {filepath}: {e}")

    print("-" * 70)

    if errores:
        print("\nErrores encontrados:")
        for error in errores:
            print(error)

    if resultados:
        # Escribir el manifiesto
        with open(output_file, 'w') as f:
            for hash_value, filename, _ in resultados:
                f.write(f"{hash_value}  {filename}\n")

        print(f"\n✓ Manifiesto generado exitosamente: {output_file}")
        print(f"  Archivos incluidos: {len(resultados)}")

        # Mostrar contenido del manifiesto
        print("\n" + "=" * 70)
        print("CONTENIDO DE SHA256SUMS.txt")
        print("=" * 70)
        with open(output_file, 'r') as f:
            print(f.read())
    else:
        print("\n✗ No se pudo generar el manifiesto: ningún archivo válido")

    return resultados


def crear_archivos_ejemplo():
    """Crea archivos de ejemplo para demostrar el funcionamiento."""
    print("\nCreando archivos de ejemplo para la demostración...")

    # Crear directorio de paquetes si no existe
    os.makedirs("paquete_medisoft", exist_ok=True)

    archivos_ejemplo = {
        "paquete_medisoft/medisoft_v2.1.0.exe": b"MediSoft Diagnostic Software v2.1.0\nBinary content simulation...\n" + b"\x00" * 100,
        "paquete_medisoft/config.xml": b"""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <version>2.1.0</version>
    <hospital_id>GT-001</hospital_id>
    <modules>
        <module name="diagnostics" enabled="true"/>
        <module name="reports" enabled="true"/>
        <module name="sync" enabled="true"/>
    </modules>
</configuration>
""",
        "paquete_medisoft/drivers/lab_device.dll": b"DLL Driver for Lab Equipment\nVersion 1.2.3\n" + b"\xFF" * 50,
        "paquete_medisoft/data/calibration.dat": b"Calibration data for diagnostic equipment\n" + bytes(range(256)),
        "paquete_medisoft/README.txt": b"""MediSoft Diagnostic Software v2.1.0
====================================

Instrucciones de instalacion:
1. Ejecute medisoft_v2.1.0.exe como administrador
2. Siga las instrucciones del asistente
3. Reinicie el equipo cuando se le solicite

Soporte: soporte@medisoft.com.gt
"""
    }

    archivos_creados = []
    for filepath, content in archivos_ejemplo.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(content)
        archivos_creados.append(filepath)
        print(f"  Creado: {filepath}")

    return archivos_creados


def main():
    if len(sys.argv) > 1:
        # Usar archivos proporcionados por línea de comandos
        archivos = sys.argv[1:]
        print(f"Procesando {len(archivos)} archivos proporcionados...")
    else:
        # Crear y usar archivos de ejemplo
        print("No se proporcionaron archivos. Creando archivos de ejemplo...\n")
        archivos = crear_archivos_ejemplo()

    if len(archivos) < 5:
        print(f"\n⚠️  Advertencia: Se requieren al menos 5 archivos.")
        print(f"   Archivos proporcionados: {len(archivos)}")
        if len(archivos) == 0:
            return

    print()
    generar_manifiesto(archivos)

    print("\n" + "=" * 70)
    print("INSTRUCCIONES PARA EL SIGUIENTE PASO")
    print("=" * 70)
    print("""
El archivo SHA256SUMS.txt ahora contiene los hashes de todos los archivos
del paquete de MediSoft.

Para verificar la integridad de los archivos descargados, ejecute:
  python verificar_paquete.py

Para probar la detección de modificaciones:
1. Modifique cualquier byte de un archivo del paquete
2. Ejecute verificar_paquete.py
3. Observe cómo se detecta la alteración
""")


if __name__ == "__main__":
    main()
