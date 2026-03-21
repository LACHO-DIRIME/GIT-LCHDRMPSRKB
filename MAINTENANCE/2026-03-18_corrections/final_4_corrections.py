#!/usr/bin/env python3
"""
Correcciones Finales de 4 Warnings - Prompts LACHO
Corrige los 4 warnings restantes de METHOD <psi_spin>
"""

import os
import re

def apply_final_4_corrections():
    """Aplica las últimas 4 correcciones necesarias"""
    
    target_file = "/media/Personal/PLANERAI/DIRIME/OPTIMIZACION DE PROMPTS  para Windsurf/$thu 19-03 to $wed 25-03_optimizar para prompts WINDSUF.txt"
    
    print("🔧 CORRIGIENDO ÚLTIMOS 4 WARNINGS")
    print("=" * 50)
    
    if not os.path.exists(target_file):
        print(f"❌ Archivo no encontrado: {target_file}")
        return
    
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Corregir METHOD <psi_spin> → METHOD <stat_onto>
    # Los 4 warnings son por <psi_spin> no canónico en METHOD
    # Lo cambiamos a <stat_onto> que es canónico y mantiene sentido semántico
    
    pattern = r'METHOD <psi_spin> =><= .. calcula ..'
    replacement = 'METHOD <stat_onto> =><= .. calcula ..'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print("✅ Corrección aplicada: METHOD <psi_spin> → <stat_onto>")
        
        # Guardar cambios
        backup_path = target_file + '.backup_4_corrections'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📋 Backup creado: {backup_path}")
        
        # Validación final
        print("\n📊 VALIDACIÓN FINAL DE 4 CORRECCIONES")
        print("-" * 40)
        
        import sys
        imv_path = "/media/Personal/PLANERAI/DIRIME/IMV"
        if imv_path not in sys.path:
            sys.path.insert(0, imv_path)
        
        from core.grammar import validate
        
        # Extraer prompts y validar
        prompts = []
        for line in content.split('\n'):
            if '=><= ..' in line and '--[' in line and '[term]' in line:
                prompts.append(line.strip())
        
        valid_count = 0
        warning_count = 0
        error_count = 0
        
        for prompt in prompts:
            try:
                result = validate(prompt)
                if result.result.value == 'VALID':
                    valid_count += 1
                warning_count += len(result.warnings) if hasattr(result, 'warnings') else 0
                error_count += len(result.errors) if hasattr(result, 'errors') else 0
            except:
                error_count += 1
        
        success_rate = (valid_count / len(prompts)) * 100 if prompts else 0
        
        print(f"📈 Total prompts: {len(prompts)}")
        print(f"✅ Prompts válidos: {valid_count}")
        print(f"⚠️  Warnings: {warning_count}")
        print(f"❌ Errors: {error_count}")
        print(f"📊 Tasa de éxito: {success_rate:.1f}%")
        
        if success_rate >= 90 and warning_count <= 2:
            print("\n🚀 ¡CORRECCIONES COMPLETADAS - EXCELENTE PARA PROCEDER!")
            print("✅ Sistema listo para deployment con alta calidad")
        elif success_rate >= 85:
            print("\n⚠️  CORRECCIONES ACEPTABLES - PROCEDER CON CONFIANZA")
            print("✅ Sistema listo para deployment")
        else:
            print("\n❌ Revisar manualmente")
            
    else:
        print("❌ No se encontraron patrones <psi_spin> para corregir")

if __name__ == "__main__":
    apply_final_4_corrections()
