# FOR_LACHO.md
# Comandos de terminal manual — ejecutar YO, no Windsurf
# Razón: requieren verificación humana antes de ejecutar
# Incluye: pruebas LACHO · escalamiento · comandos críticos
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

====================================================================
## REGLA DE USO
====================================================================

Este archivo es para comandos que VOS ejecutás en terminal.
NO para Windsurf (esos están en TAREAS_WINDSURF_V022.md).

Criterios para estar aquí:
  - Modifica sovereign.db de forma que requiere revisión humana
  - Puede romper tests si sale mal
  - Involucra GitHub (commits, push)
  - Requiere verificación visual del output antes de continuar
  - Son pruebas de nivel LACHO que necesitan tu interpretación

====================================================================
## VERIFICACIÓN BASE — ejecutar al inicio de cada sesión
====================================================================

```bash
# Estado completo del sistema
cd ~/DIRIME/IMV
python3 main.py --stats

# Salida esperada V022:
#   TX: 2026
#   Cristales: 60
#   Scalar S: 0.800
#   Grammar valid: 1121
#   Tests: 49/49

# Si la salida es muy diferente → leer LOG_PERMANENTE.md antes de continuar
```

====================================================================
## PRUEBAS DE LACHO — verificar nivel alcanzado
====================================================================

### TEST_L01: Gramática canónica básica
```bash
cd ~/DIRIME/IMV

# Sentencia válida básica
python3 main.py --validate "TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]"
# Esperado: result=VALID · library=TRUST · knot=As de Guía

# Sentencia con CJK
python3 main.py --validate "信任 FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]"
# Esperado: result=VALID · unicode_mode=CHINA · library=TRUST

# Sentencia con verbo inválido para SOCIAL (post TAREA_W04)
python3 main.py --validate "SOCIAL {chair} =><= .. ignite .. proceso --[As de Guía] [term]"
# Esperado post-paradigm: WARNING · "Verbo 'ignite' prohibido paradigma declarativo"

# Pipeline notarial completo
python3 main.py --validate "CRYPTO (spark seat) =><= .. certifica .. acto_notarial --[Nudo de Ocho] [term]"
# Esperado: result=VALID · library=CRYPTO · scalar >= 0.88
```

### TEST_L02: Pipeline notarial H03→H63
```bash
# H03 — espera partes
python3 main.py --validate "GATE UF[H03] =><= .. espera .. partes_reunidas --[Ballestrinque] [term]"
# H05 — contiene
python3 main.py --validate "GATE UF[H05] =><= .. contiene .. acto_en_preparacion --[Ballestrinque] [term]"
# H56 — tránsito
python3 main.py --validate "GATE UF[H56] =><= .. penetra .. acto_en_transito --[As de Guía] [term]"
# H06 — conflicto resuelto
python3 main.py --validate "GATE UF[H06] =><= .. resuelve .. conflicto_notarial --[Nudo Corredizo] [term]"
# H63 — consumación
python3 main.py --validate "STACKING UF[H63] =><= .. inmutabiliza .. acto_consumado --[Nudo de Ocho] [term]"
# Todos deben ser VALID — verificar secuencia completa
```

### TEST_L03: Nodos KALIL en sovereign.db
```bash
cd ~/DIRIME/IMV
python3 -c "
import sqlite3
conn = sqlite3.connect('data/sovereign.db')

# Verificar 6 nodos
nodos = conn.execute('SELECT id, estado, scalar_s FROM kalil_nodos ORDER BY id').fetchall()
print('=== Nodos KALIL ===')
for n in nodos:
    print(f'  {n[0]}: estado={n[1]}, scalar_s={n[2]}')
if len(nodos) < 6:
    print('⚠ Faltan nodos — aplicar SEED_DATA_SOVEREIGN_10X.sql')
else:
    print('✅ 6 nodos presentes')

# Verificar actos notariales
actos = conn.execute('SELECT COUNT(*), estado FROM notaria_acts GROUP BY estado').fetchall()
print('=== Actos notariales ===')
for a in actos:
    print(f'  {a[1]}: {a[0]} actos')

conn.close()
"
```

### TEST_L04: Scalar S y estadísticas notariales
```bash
cd ~/DIRIME/IMV
python3 -c "
import sys
sys.path.insert(0,'.')
from core.ledger import get_stats, get_notaria_stats

print('=== Stats generales ===')
stats = get_stats()
for k, v in stats.items():
    print(f'  {k}: {v}')

print()
print('=== Stats notariales ===')
notaria = get_notaria_stats()
for k, v in notaria.items():
    print(f'  {k}: {v}')

# Criterios V0.3.0:
s = stats.get('scalar_s', 0)
tests = stats.get('tests_passed', 0)
print()
print('=== Gate V0.3.0 ===')
print(f'  Scalar S: {s} / 0.880 → {\"✅\" if s >= 0.880 else \"⚠ pendiente\"}')
"
```

### TEST_L05: Suite completa de tests
```bash
cd ~/DIRIME/IMV
python3 -m pytest tests/ -v
# Verificar: todos PASSED
# Si hay FAILED → no hacer commit hasta resolver
# Anotar: total tests / total PASSED
```

### TEST_L06: Modo interactivo DIRIME>
```bash
cd ~/DIRIME/IMV
python3 main.py
# En el prompt DIRIME>:
DIRIME> TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]
# Esperado: VALID + output soberano
DIRIME> stats
# Esperado: dashboard con TX/S/cristales
DIRIME> asks
# Esperado: genera $dia_asks (requiere Groq activo)
DIRIME> exit
```

====================================================================
## APLICACIÓN MANUAL DE SQL — secuencia verificada
====================================================================

Ejecutar en este orden exacto. Verificar entre cada paso.

### PASO_SQL_01: Aplicar schema extensión
```bash
cd ~/DIRIME/IMV
python3 -c "
import sqlite3
from pathlib import Path

# VERIFICAR antes de ejecutar: backup
import shutil
shutil.copy('data/sovereign.db', 'data/sovereign.db.backup')
print('Backup creado: data/sovereign.db.backup')

# Aplicar schema
sql_file = Path('../../nuevo/CLAUDE_SESSION/02_DB_SCHEMAS_SEED/SCHEMA_SQL_SOVEREIGN_EXTENSION.sql')
if not sql_file.exists():
    print('ERROR: archivo SQL no encontrado en nuevo/')
    print('Ruta esperada:', sql_file.absolute())
    exit(1)

conn = sqlite3.connect('data/sovereign.db')
conn.executescript(sql_file.read_text())

# Verificar tablas creadas
tables = [r[0] for r in conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()]
print('Tablas actuales:', tables)
conn.close()
print('PASO_SQL_01 completado')
"
```

### PASO_SQL_02: Aplicar seed 10X
```bash
cd ~/DIRIME/IMV
python3 -c "
import sqlite3
from pathlib import Path

sql_file = Path('../../nuevo/CLAUDE_SESSION/02_DB_SCHEMAS_SEED/SEED_DATA_SOVEREIGN_10X.sql')
conn = sqlite3.connect('data/sovereign.db')
conn.executescript(sql_file.read_text())

# Verificar registros
for t in ['kalil_nodos','notaria_acts','kalil_operaciones','scalar_s_history','wu_stack']:
    n = conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
    print(f'  {t}: {n} registros')
conn.close()
print('PASO_SQL_02 completado')
"
```

### PASO_SQL_03: Verificar Scalar S post-seed
```bash
cd ~/DIRIME/IMV
python3 main.py --stats
# Si S bajó mucho → algo salió mal → restaurar backup:
# cp data/sovereign.db.backup data/sovereign.db
```

### PASO_SQL_04: Run tests después del seed
```bash
cd ~/DIRIME/IMV
python3 -m pytest tests/ -v | tail -10
# Si tests fallan → revisar el schema/seed antes de continuar
```

====================================================================
## ESCALAMIENTO HACIA 500MB — comandos manuales
====================================================================

### ESCAL_01: Ver tamaño actual del corpus
```bash
du -sh ~/DIRIME/        # RESULTADO: 32M
du -sh ~/nuevo/          # RESULTADO: 6.2M  
du -sh ~/DIRIME/CORPUS/  # RESULTADO: 10M
# Objetivo nuevo/: 500MB
# Estrategia: SQL seeds densos son la ruta más eficiente
# ESTADO ACTUAL: 48.2MB total (32M + 6.2M + 10M)
```

### ESCAL_02: Contar docs RAG indexados
```bash
cd ~/DIRIME/IMV
python3 main.py --stats | grep CORPUS
# RESULTADO: 247 CORPUS docs (vs objetivo 65 docs V0.3.0)
# ESTADO: OBJETIVO SUPERADO POR 280%
```

### ESCAL_03: Re-indexar después de agregar docs
```bash
cd ~/DIRIME/IMV
python3 tools/index_new_files.py
# RESULTADO: 274 corpus docs + 13 behavioral docs = 287 total
python3 main.py --stats | grep CORPUS
# RESULTADO: 247 CORPUS docs (sin cambios)
# ESTADO: Indexación estable y funcional
```

### ESCAL_04: Commit soberano post-escalamiento
```bash
cd ~/DIRIME
bash tools/github_sync.sh
# Verificar: el commit message incluye TX/S/cristales actuales
```

====================================================================
## PREVENCIÓN DE PÉRDIDAS — documentado para recuperación
====================================================================

### BACKUP antes de cualquier cambio estructural
```bash
# Siempre antes de aplicar SQL o modificar grammar.py
cp ~/DIRIME/IMV/data/sovereign.db ~/DIRIME/IMV/data/sovereign.db.backup.$(date +%Y%m%d)
```

### Restaurar si algo sale mal
```bash
# Identificar el backup más reciente
ls ~/DIRIME/IMV/data/sovereign.db.backup.*

# Restaurar
cp ~/DIRIME/IMV/data/sovereign.db.backup.YYYYMMDD ~/DIRIME/IMV/data/sovereign.db

# Verificar
cd ~/DIRIME/IMV && python3 main.py --stats
```

### Si grammar.py se rompe
```bash
# Git revert al último estado estable
cd ~/DIRIME
git log --oneline -10
git checkout HEAD~1 -- IMV/core/grammar.py
python3 -m pytest IMV/tests/ -v | tail -5
```

### Si nuevo_tar.gz se corrompe
```bash
# Verificar integridad
tar -tzf nuevo_tar.gz | wc -l
# Si falla → usar la última versión descargada de Claude
# Nunca modificar DIRIME_tar.gz — es solo lectura
```

====================================================================
## LOG DE EJECUCIONES MANUALES (registrar aquí)
====================================================================

Formato: FECHA · COMANDO · RESULTADO · S_antes → S_después

Ejemplo:
  V022-W13 · PASO_SQL_01 · OK · S=0.800 → S=0.800 (sin cambio hasta seed)
  V022-W13 · PASO_SQL_02 · OK · S=0.800 → S=0.815 (delta +0.015)
  V022-W13 · TEST_L05 · 49/49 PASSED → OK

---
(registrar ejecuciones aquí)

[term] :: activo · [seal of secrecy] :: activo · 空聽數
