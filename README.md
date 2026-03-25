# Ejercicio de Hashes y Firmas Digitales
Michelle Mejía Villela


**Universidad del Valle de Guatemala**
**Cifrados de Información**

## Descripción del Proyecto

Este proyecto implementa un sistema de verificación de integridad y autenticidad para MediSoft S.A., una empresa que distribuye software de diagnóstico a hospitales en Guatemala, Honduras y El Salvador.

El sistema aborda dos capas de protección basadas en hashes y firmas digitales:

1. **Integridad de distribución**: Verificar que los paquetes descargados son exactamente los que MediSoft publicó.
2. **Autenticación de origen**: Garantizar que el manifiesto de hashes fue creado exclusivamente por MediSoft.

## Estructura del Proyecto

```
scripts/
├── explorar_hashes.py      # Ejercicio 1: Comparación de algoritmos de hash
├── verificar_passwords.py  # Ejercicio 2: Verificación en Have I Been Pwned
├── generar_manifiesto.py   # Ejercicio 3a: Generación de manifiesto SHA-256
├── verificar_paquete.py    # Ejercicio 3b: Verificación de integridad
├── generar_claves_rsa.py   # Ejercicio 4: Generación de claves y firma digital
├── verificar_firma.py      # Ejercicio 5: Verificación de autenticidad
└── README.md               # Este archivo
```

## Instrucciones de Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
pip install pycryptodome requests
```

O usando un archivo requirements.txt:

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
pycryptodome>=3.20.0
requests>=2.31.0
```

## Instrucciones de Uso

### Ejercicio 1: Comparación de Algoritmos de Hash

```bash
python explorar_hashes.py
```

Este script:
- Calcula hashes MD5, SHA-1, SHA-256 y SHA-3/256
- Muestra una tabla comparativa
- Analiza el efecto avalancha usando XOR

### Ejercicio 2: Verificación de Contraseñas (HIBP)

```bash
python verificar_passwords.py
```

Este script:
- Verifica contraseñas comunes en Have I Been Pwned
- Usa el modelo k-Anonymity (solo envía 5 caracteres del hash)
- Muestra cuántas veces aparece cada contraseña en filtraciones

### Ejercicio 3: Verificación de Integridad

**Paso 1: Generar el manifiesto (rol de MediSoft)**
```bash
python generar_manifiesto.py
```

O con archivos específicos:
```bash
python generar_manifiesto.py archivo1.txt archivo2.exe archivo3.dll archivo4.xml archivo5.dat
```

**Paso 2: Verificar el paquete (rol del hospital)**
```bash
python verificar_paquete.py
```

**Paso 3: Probar detección de modificaciones**
```bash
python verificar_paquete.py --modificar
python verificar_paquete.py
```

### Ejercicio 4: Generación de Claves y Firma Digital

```bash
python generar_claves_rsa.py
```

Este script:
- Genera un par de claves RSA de 2048 bits
- Guarda la clave privada en `medisoft_priv.pem`
- Guarda la clave pública en `medisoft_pub.pem`
- Firma el manifiesto SHA256SUMS.txt
- Genera la firma en `SHA256SUMS.sig`

### Ejercicio 5: Verificación de Firma Digital

```bash
python verificar_firma.py
```

**Probar detección de alteración del manifiesto:**
```bash
python verificar_firma.py --modificar
python verificar_firma.py
```

## Ejemplos de Ejecución

### Ejemplo 1: Exploración de Hashes

```
$ python explorar_hashes.py

========================================================
EJERCICIO 1: COMPARACIÓN DE ALGORITMOS DE HASH
========================================================

Texto                     Algoritmo    Bits     Hex    Hash
--------------------------------------------------------
MediSoft-v2.1.0          MD5          128      32     a1b2c3d4e5f6...
                          SHA-1        160      40     1a2b3c4d5e6f...
                          SHA-256      256      64     abcd1234efgh...
                          SHA-3/256    256      64     5678ijkl9012...
--------------------------------------------------------
medisoft-v2.1.0          MD5          128      32     x1y2z3a4b5c6...
                          ...

ANÁLISIS DE DIFERENCIAS (SHA-256)
Bits diferentes (usando XOR): ~128 de 256 (50%)
```

### Ejemplo 2: Verificación de Contraseñas

```
$ python verificar_passwords.py

Contraseña           SHA-256 Hash                                        Filtraciones
-----------------------------------------------------------------------------------
admin                8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918   42,678,423 veces
123456               8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92   37,359,195 veces
hospital             ...                                                                  1,234 veces
medisoft2024         ...                                                                  No encontrada
```

### Ejemplo 3: Verificación de Integridad

```
$ python verificar_paquete.py

VERIFICADOR DE INTEGRIDAD - Hospital IT Admin
==================================================

  ✓  OK: medisoft_v2.1.0.exe
  ✓  OK: config.xml
  ✓  OK: drivers/lab_device.dll
  ✓  OK: data/calibration.dat
  ✓  OK: README.txt

RESUMEN:
  Total: 5 archivos
  ✓ Verificados correctamente: 5
  ✗ Verificación fallida: 0

✓ VERIFICACIÓN EXITOSA
```

### Ejemplo 4: Detección de Archivo Modificado

```
$ python verificar_paquete.py --modificar
$ python verificar_paquete.py

  ✓  OK: medisoft_v2.1.0.exe
  ✗  FALLIDO: config.xml
      Esperado: abc123...
      Actual:   def456...

⚠️ ALERTA DE SEGURIDAD: ARCHIVOS MODIFICADOS DETECTADOS
```

### Ejemplo 5: Verificación de Firma Digital

```
$ python verificar_firma.py

VERIFICADOR DE FIRMA DIGITAL
============================

Verificando archivos requeridos:
  ✓ Manifiesto de hashes: SHA256SUMS.txt
  ✓ Firma digital: SHA256SUMS.sig
  ✓ Clave pública de MediSoft: medisoft_pub.pem

VERIFICANDO FIRMA...

✓ FIRMA VÁLIDA

La firma digital es VÁLIDA. Esto garantiza:
1. AUTENTICIDAD: El manifiesto fue creado por MediSoft S.A.
2. INTEGRIDAD: El manifiesto NO ha sido modificado
```

---

## Respuestas a Preguntas de Análisis

### Ejercicio 1: ¿Cuántos bits cambiaron entre los dos hashes SHA-256?

**Respuesta:** Aproximadamente 128 bits (50% del total de 256 bits).

**Propiedad demostrada:** **Efecto Avalancha** (Avalanche Effect)
- Un cambio mínimo en la entrada (solo mayúsculas/minúsculas) produce un cambio drástico en la salida.
- Idealmente, ~50% de los bits deberían cambiar.
- Esto hace imposible predecir cómo cambiará el hash basándose en el cambio de entrada.

### Ejercicio 1: ¿Por qué MD5 es considerado inseguro para integridad de archivos?

**Respuesta basada en la longitud de bits:**

1. **Vulnerabilidad a colisiones:** Con 128 bits, por la paradoja del cumpleaños, se necesitan solo 2^64 operaciones para encontrar una colisión. En 2004 se demostraron colisiones prácticas en MD5.

2. **Comparación con alternativas seguras:**
   - MD5: 128 bits (2^64 para colisiones)
   - SHA-256: 256 bits (2^128 para colisiones)
   - MD5 es 2^64 veces más fácil de atacar que SHA-256.

3. **Riesgo para MediSoft:** Un atacante podría crear archivos maliciosos con el mismo hash MD5, comprometiendo equipos médicos críticos.

### Ejercicio 5: ¿Por qué la firma es válida después de modificar un archivo de datos?

**Respuesta:**

La firma digital firma únicamente el **contenido del manifiesto** (`SHA256SUMS.txt`), NO los archivos de datos directamente.

**Sistema de dos capas:**

| Capa | Verificación | Detecta |
|------|--------------|---------|
| 1. Autenticidad (`verificar_firma.py`) | Firma RSA del manifiesto | Modificación del manifiesto |
| 2. Integridad (`verificar_paquete.py`) | Hashes SHA-256 de archivos | Modificación de archivos |

**Por lo tanto:**
- Si se modifica un **archivo de datos**: La firma es válida (manifiesto no cambió), pero `verificar_paquete.py` detecta que el hash no coincide.
- Si se modifica el **manifiesto**: `verificar_firma.py` detecta inmediatamente que la firma es inválida.

**Conclusión:** Ambas verificaciones son necesarias para seguridad completa. Un atacante no puede evadir ambas capas simultáneamente.

---

## Recursos Adicionales

- [Documentación de pycryptodome](https://pycryptodome.readthedocs.io)
- [RFC 8017 — PKCS#1 v2.2](https://www.rfc-editor.org/rfc/rfc8017)
- [Presentaciones del curso](https://locano-uvg.github.io/cifrados-26/)
- Open AI. Modelo de Chatgpt versión marzo del 2026.