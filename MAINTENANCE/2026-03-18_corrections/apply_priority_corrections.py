#!/usr/bin/env python3
"""
Aplicar Correcciones Prioritarias - Prompts LACHO
Corrige manualmente los WARNINGs críticos identificados
"""

import os
import re
from typing import Dict, List

class PriorityCorrector:
    """Aplica correcciones prioritarias a prompts LACHO"""
    
    def __init__(self):
        self.corrections_log = []
    
    def apply_corrections_to_file(self, file_path: str) -> Dict:
        """Aplica correcciones a un archivo de prompts"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Corrección 1: SOCIAL - planifica → distribuye
            content = self._correct_social_planifica(content)
            
            # Corrección 2: STACKING - aquieta → cristaliza  
            content = self._correct_stacking_aquieta(content)
            
            # Corrección 3: WORK - {door} → {door-afternoon}
            content = self._correct_work_door(content)
            
            # Corrección 4: WORK - abre → materializa
            content = self._correct_work_abre(content)
            
            # Guardar archivo corregido
            if content != original_content:
                backup_path = file_path + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return {
                    'success': True,
                    'corrections_applied': len(self.corrections_log),
                    'backup_created': backup_path,
                    'corrections': self.corrections_log
                }
            else:
                return {
                    'success': True,
                    'corrections_applied': 0,
                    'message': 'No corrections needed'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _correct_social_planifica(self, content: str) -> str:
        """Corrige 'planifica' → 'distribuye' en sentencias SOCIAL"""
        pattern = r'(SOCIAL \{scheduler\}\s*=><=\s*\.\.\s*)planifica'
        replacement = r'\1distribuye'
        
        if re.search(pattern, content):
            self.corrections_log.append("SOCIAL {scheduler}: planifica → distribuye")
            return re.sub(pattern, replacement, content)
        return content
    
    def _correct_stacking_aquieta(self, content: str) -> str:
        """Corrige 'aquieta' → 'cristaliza' en sentencias STACKING"""
        pattern = r'(STACKING UF\[H\d+\]\s*=><=\s*\.\.\s*)aquieta'
        replacement = r'\1cristaliza'
        
        if re.search(pattern, content):
            self.corrections_log.append("STACKING UF[H##]: aquieta → cristaliza")
            return re.sub(pattern, replacement, content)
        return content
    
    def _correct_work_door(self, content: str) -> str:
        """Corrige '{door}' → '{door-afternoon}' en sentencias WORK"""
        pattern = r'WORK \{door\}\s*=><='
        replacement = 'WORK {door-afternoon} =>=<='
        
        if re.search(pattern, content):
            self.corrections_log.append("WORK: {door} → {door-afternoon}")
            return re.sub(pattern, replacement, content)
        return content
    
    def _correct_work_abre(self, content: str) -> str:
        """Corrige 'abre' → 'materializa' en sentencias WORK"""
        pattern = r'(WORK \{[^}]+\}\s*=><=\s*\.\.\s*)abre'
        replacement = r'\1materializa'
        
        if re.search(pattern, content):
            self.corrections_log.append("WORK: abre → materializa")
            return re.sub(pattern, replacement, content)
        return content
    
    def validate_corrections(self, file_path: str) -> Dict:
        """Valida las correcciones aplicadas"""
        try:
            import sys
            imv_path = "/media/Personal/PLANERAI/DIRIME/IMV"
            if imv_path not in sys.path:
                sys.path.insert(0, imv_path)
            
            from core.grammar import validate
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraer prompts LACHO
            prompts = []
            for line in content.split('\n'):
                if '=><= ..' in line and '--[' in line and '[term]' in line:
                    prompts.append(line.strip())
            
            validation_results = []
            for i, prompt in enumerate(prompts):
                try:
                    result = validate(prompt)
                    validation_results.append({
                        'index': i + 1,
                        'prompt': prompt,
                        'valid': result.result.value == 'VALID',
                        'warnings': len(result.warnings) if hasattr(result, 'warnings') else 0,
                        'errors': len(result.errors) if hasattr(result, 'errors') else 0,
                        'library': result.library.value if hasattr(result, 'library') else 'UNKNOWN'
                    })
                except Exception as e:
                    validation_results.append({
                        'index': i + 1,
                        'prompt': prompt,
                        'valid': False,
                        'warnings': 0,
                        'errors': 1,
                        'library': 'ERROR',
                        'error': str(e)
                    })
            
            # Calcular estadísticas
            total = len(validation_results)
            valid = sum(1 for r in validation_results if r['valid'])
            total_warnings = sum(r['warnings'] for r in validation_results)
            total_errors = sum(r['errors'] for r in validation_results)
            
            return {
                'total_prompts': total,
                'valid_prompts': valid,
                'invalid_prompts': total - valid,
                'total_warnings': total_warnings,
                'total_errors': total_errors,
                'success_rate': (valid / total) * 100 if total > 0 else 0,
                'validation_results': validation_results
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'total_prompts': 0,
                'valid_prompts': 0,
                'success_rate': 0
            }

def main():
    """Función principal"""
    corrector = PriorityCorrector()
    
    # Archivo a corregir
    target_file = "/media/Personal/PLANERAI/DIRIME/OPTIMIZACION DE PROMPTS  para Windsurf/$thu 19-03 to $wed 25-03_optimizar para prompts WINDSUF.txt"
    
    print("🔧 APLICANDO CORRECCIONES PRIORITARIAS")
    print("=" * 60)
    
    if not os.path.exists(target_file):
        print(f"❌ Archivo no encontrado: {target_file}")
        return
    
    # Aplicar correcciones
    print(f"📁 Procesando: {target_file}")
    result = corrector.apply_corrections_to_file(target_file)
    
    if result['success']:
        corrections = result['corrections_applied']
        print(f"✅ Correcciones aplicadas: {corrections}")
        
        if corrections > 0:
            print(f"📋 Backup creado: {result['backup_created']}")
            print("\n🔧 Correcciones aplicadas:")
            for correction in result['corrections']:
                print(f"   • {correction}")
        
        # Validar resultados
        print("\n📊 Validando correcciones...")
        validation = corrector.validate_corrections(target_file)
        
        if 'error' not in validation:
            print(f"📈 Total prompts: {validation['total_prompts']}")
            print(f"✅ Prompts válidos: {validation['valid_prompts']}")
            print(f"⚠️  Warnings totales: {validation['total_warnings']}")
            print(f"❌ Errors totales: {validation['total_errors']}")
            print(f"📊 Tasa de éxito: {validation['success_rate']:.1f}%")
            
            # Verificar si es seguro proceder
            if validation['success_rate'] >= 90:
                print("\n🚀 ¡Correcciones exitosas - seguro proceder!")
            elif validation['success_rate'] >= 80:
                print("\n⚠️  Correcciones aceptables - proceder con cuidado")
            else:
                print("\n❌ Revisar errores restantes manualmente")
        else:
            print(f"❌ Error en validación: {validation['error']}")
    else:
        print(f"❌ Error aplicando correcciones: {result['error']}")

if __name__ == "__main__":
    main()
