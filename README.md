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
pip install -r requirements.txt
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

```bash
============================================================
EJERCICIO 1: COMPARACIÓN DE ALGORITMOS DE HASH
MediSoft S.A. - Verificación de Integridad
============================================================

========================================================================================================================
Texto                     Algoritmo    Bits     Hex    Hash
========================================================================================================================
MediSoft-v2.1.0           MD5          128      32     cac2fe40370e3a68f0a4927c20c75c89
                          SHA-1        160      40     3ab92abc44e23465b154e887f90c3a5e0d642c65
                          SHA-256      256      64     64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996
                          SHA-3/256    256      64     3b0af4c0a9078e2ddc1606313db9206dcb3a4dbf423d78c0cf16929d303e30d2
------------------------------------------------------------------------------------------------------------------------
medisoft-v2.1.0           MD5          128      32     fa386a0d796e388b24cb3302c185a445
                          SHA-1        160      40     4fe9fa8c97db362ecce61ee6302a92f0505217cd
                          SHA-256      256      64     ec8d163da33b9832c33fbb2d7cba98f5a7087aa6cbdecc04eb32810b1f1f895e
                          SHA-3/256    256      64     569daf2d0645c0ab6c0a7960cb552f28ac1a222284fa5605ab11cfe0a2dce82c
------------------------------------------------------------------------------------------------------------------------

============================================================
ANÁLISIS DE DIFERENCIAS (SHA-256)
============================================================

Hash SHA-256 de 'MediSoft-v2.1.0':
  64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996

Hash SHA-256 de 'medisoft-v2.1.0':
  ec8d163da33b9832c33fbb2d7cba98f5a7087aa6cbdecc04eb32810b1f1f895e

Bits diferentes (usando XOR): 120 de 256 (46.88%)

============================================================
RESPUESTAS A PREGUNTAS DE ANÁLISIS
============================================================

PREGUNTA 1: ¿Cuántos bits cambiaron entre los dos hashes SHA-256?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Respuesta: 120 bits cambiaron de un total de 256 bits.

Esto representa aproximadamente el 46.88% del hash total.

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
```

### Ejercicio 2: Verificación de Contraseñas (HIBP)

```bash
python verificar_passwords.py
```

Este script:
- Verifica contraseñas comunes en Have I Been Pwned
- Usa el modelo k-Anonymity (solo envía 5 caracteres del hash)
- Muestra cuántas veces aparece cada contraseña en filtraciones

```bash
================================================================================
EJERCICIO 2: VERIFICACIÓN DE CONTRASEÑAS EN HAVE I BEEN PWNED
MediSoft S.A. - Seguridad de Credenciales
================================================================================

--------------------------------------------------------------------------------
Contraseña           SHA-256 Hash                                                       Filtraciones
--------------------------------------------------------------------------------
admin                8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918   42,085,691 veces
123456               8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92   209,972,844 veces
hospital             8afe3c83decffdf6dc48597a3f1a52be7c6e2b97b4bdf3b15e20a87a1f657f01   118,791 veces
medisoft2024         78c12e8e24dfd7836c748c33dff2e9150c028d69488f203485e13f4a6daa777c   No encontrada
--------------------------------------------------------------------------------

================================================================================
DETALLES DE LA VERIFICACIÓN (k-Anonymity)
================================================================================

Contraseña: 'admin'
  SHA-1:   D033E22AE348AEB5660FC2140AEC35850C4DA997
  SHA-256: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
  Prefijo enviado a HIBP (SHA-1): D033E
  Sufijo buscado localmente:      22AE348AEB5660FC2140AEC35850C4DA997
  ⚠️  ADVERTENCIA: Esta contraseña ha sido expuesta 42,085,691 veces

Contraseña: '123456'
  SHA-1:   7C4A8D09CA3762AF61E59520943DC26494F8941B
  SHA-256: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
  Prefijo enviado a HIBP (SHA-1): 7C4A8
  Sufijo buscado localmente:      D09CA3762AF61E59520943DC26494F8941B
  ⚠️  ADVERTENCIA: Esta contraseña ha sido expuesta 209,972,844 veces

Contraseña: 'hospital'
  SHA-1:   2B2D005E88CE14A4112785BB266B2C0C16BE7EB4
  SHA-256: 8afe3c83decffdf6dc48597a3f1a52be7c6e2b97b4bdf3b15e20a87a1f657f01
  Prefijo enviado a HIBP (SHA-1): 2B2D0
  Sufijo buscado localmente:      05E88CE14A4112785BB266B2C0C16BE7EB4
  ⚠️  ADVERTENCIA: Esta contraseña ha sido expuesta 118,791 veces

Contraseña: 'medisoft2024'
  SHA-1:   F80CF41ABF90CAA2EC08527F641C40B4ABFE4DB9
  SHA-256: 78c12e8e24dfd7836c748c33dff2e9150c028d69488f203485e13f4a6daa777c
  Prefijo enviado a HIBP (SHA-1): F80CF
  Sufijo buscado localmente:      41ABF90CAA2EC08527F641C40B4ABFE4DB9
  ✓  Esta contraseña no aparece en filtraciones conocidas

================================================================================
ANÁLISIS DE SEGURIDAD
================================================================================

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
```

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

```bash
PS C:\Users\usuario\Desktop\U\Cifrados\Hashes-Cifrados> python verificar_paquete.py
======================================================================
VERIFICADOR DE INTEGRIDAD - Hospital IT Admin
======================================================================

Manifiesto: SHA256SUMS.txt
Directorio: paquete_medisoft
Archivos a verificar: 5

----------------------------------------------------------------------
RESULTADOS DE VERIFICACIÓN
----------------------------------------------------------------------
  ✓  OK: medisoft_v2.1.0.exe
  ✓  OK: config.xml
  ✓  OK: lab_device.dll
  ✓  OK: calibration.dat
  ✓  OK: README.txt

======================================================================
RESUMEN DE VERIFICACIÓN
======================================================================

  Total de archivos en manifiesto: 5
  ✓ Verificados correctamente:     5
  ✗ Verificación fallida:          0
  ⚠️  No encontrados:               0

  ✓ VERIFICACIÓN EXITOSA
    Todos los archivos coinciden con el manifiesto de MediSoft
    El paquete es seguro para instalar
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


```bash
PS C:\Users\usuario\Desktop\U\Cifrados\Hashes-Cifrados> python generar_claves_rsa.py
======================================================================
GENERADOR DE CLAVES RSA - MediSoft S.A.
======================================================================

Generando par de claves RSA de 2048 bits...
(Esto puede tomar unos segundos)

✓ Clave PRIVADA guardada en: medisoft_priv.pem
  ⚠️  ADVERTENCIA: ¡NO COMPARTA ESTE ARCHIVO!
  Esta clave debe mantenerse segura y confidencial.

✓ Clave PÚBLICA guardada en: medisoft_pub.pem
  Esta clave puede compartirse con los hospitales.

----------------------------------------------------------------------
INFORMACIÓN DE LAS CLAVES GENERADAS
----------------------------------------------------------------------

Tamaño de clave: 2048 bits
Módulo (n): 2048 bits
Exponente público (e): 65537

----------------------------------------------------------------------
CLAVE PÚBLICA (medisoft_pub.pem):
----------------------------------------------------------------------
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoTVLjpWJpZaQIxb/aX97
qG9HjKYq1YLhsNQs1zQJSlsVdeOT8V/934bkp/n5J6EuU+IpIiTZn+Zvi+Vf/wgF
H55suuB+dAcV0isWNpPdVLgx2zbqoPXM2vrLf7VUVwSA4YmfJKmYqIiWomwRslpk
XFJy9k77DuJJ1b9+lh4e1f5JciT9TmSoqG1WuIGeVbx9Y+gIymDW47zcGY/spSnJ
3a0tkPc+OyeKDYVdZ5QbRUfa8TK70wg4rQmPhgabY3KM2wtwgMJtEB88nzd+ZpUR
hN0xrIZZyaZzJAPkSmeMGl6YQ4HHsD6RdZA98/p66lJKYSjiAk8dKskAzLp2xrGj
dQIDAQAB
-----END PUBLIC KEY-----

----------------------------------------------------------------------
CLAVE PRIVADA (medisoft_priv.pem) - VISTA PARCIAL:
----------------------------------------------------------------------
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAoTVLjpWJpZaQIxb/aX97qG9H... [CONTENIDO OCULTO POR SEGURIDAD]
...
gwJz6Hg//kxmFqUDD8PK9bsUN2fHX8Aqz/sXt5Q1...
-----END RSA PRIVATE KEY-----

======================================================================
FIRMA DIGITAL DEL MANIFIESTO
======================================================================

Manifiesto a firmar: SHA256SUMS.txt
Tamaño: 408 bytes
SHA-256 del manifiesto: 31c3647b4d1d7ad3c5a482846d43f083e11eb7517abe1e2c9a47a6f7cc4298cb

Clave privada cargada: medisoft_priv.pem
Esquema de firma: PKCS#1 v1.5

✓ Firma guardada en: SHA256SUMS.sig
  Tamaño de firma: 256 bytes (2048 bits)

Firma (hex):
  74d2327e39f473144c8afb92a406e0e7accd1331ef0de20ea74c95f848b3e28e...
  ...2fb9305c6355776818ecb1e92a736b996c2d8c5b02811737fb43fd6e74984d4b

======================================================================
SIGUIENTE PASO
======================================================================

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
```

### Ejercicio 5: Verificación de Firma Digital

```bash
python verificar_firma.py
```

**Probar detección de alteración del manifiesto:**
```bash
python verificar_firma.py --modificar
python verificar_firma.py
```

```bash
PS C:\Users\usuario\Desktop\U\Cifrados\Hashes-Cifrados> python verificar_firma.py
======================================================================
VERIFICADOR DE FIRMA DIGITAL - Hospital IT Admin
======================================================================

Verificando archivos requeridos:
  ✓ Manifiesto de hashes: SHA256SUMS.txt
  ✓ Firma digital: SHA256SUMS.sig
  ✓ Clave pública de MediSoft: medisoft_pub.pem

----------------------------------------------------------------------
CARGANDO CLAVE PÚBLICA
----------------------------------------------------------------------
Clave pública cargada exitosamente
  Tamaño: 2048 bits
  Exponente (e): 65537

----------------------------------------------------------------------
LEYENDO MANIFIESTO
----------------------------------------------------------------------
Manifiesto: SHA256SUMS.txt
Tamaño: 408 bytes
SHA-256: 31c3647b4d1d7ad3c5a482846d43f083e11eb7517abe1e2c9a47a6f7cc4298cb

----------------------------------------------------------------------
LEYENDO FIRMA
----------------------------------------------------------------------
Firma: SHA256SUMS.sig
Tamaño: 256 bytes

----------------------------------------------------------------------
VERIFICANDO FIRMA
----------------------------------------------------------------------

======================================================================
✓ FIRMA VÁLIDA
======================================================================

La firma digital es VÁLIDA. Esto garantiza que:

1. AUTENTICIDAD: El manifiesto fue creado por MediSoft S.A.
   (Solo quien posee la clave privada puede generar esta firma)

2. INTEGRIDAD: El manifiesto NO ha sido modificado desde que fue firmado
   (Cualquier cambio invalidaría la firma)

El manifiesto es auténtico y confiable.
Puede proceder a verificar los archivos del paquete.


----------------------------------------------------------------------
SIGUIENTE PASO
----------------------------------------------------------------------

Ahora que ha verificado la autenticidad del manifiesto, puede verificar
la integridad de los archivos del paquete:

  python verificar_paquete.py


======================================================================
DEMOSTRACIÓN: Prueba de detección de alteraciones
======================================================================

Para demostrar que la firma detecta cualquier modificación:

1. Modificar el manifiesto:
   python verificar_firma.py --modificar
   python verificar_firma.py

2. O manualmente:
   - Abra SHA256SUMS.txt con un editor
   - Cambie un solo carácter de cualquier hash
   - Guarde el archivo
   - Ejecute: python verificar_firma.py


======================================================================
RESPUESTA A LA PREGUNTA DE ANÁLISIS
======================================================================

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
```

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