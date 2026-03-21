#!/usr/bin/env python3
"""
Correcciones Finales Prioritarias - Prompts LACHO
Corrige todos los WARNINGs identificados para alcanzar 90%+ de éxito
"""

import os
import re
from typing import Dict, List

class FinalPriorityCorrector:
    """Aplica correcciones finales prioritarias"""
    
    def __init__(self):
        self.corrections_applied = []
    
    def apply_all_corrections(self, file_path: str) -> Dict:
        """Aplica todas las correcciones necesarias"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Correcciones METHOD - verbos no naturales
            content = self._correct_method_verbs(content)
            
            # Correcciones WORK - sujetos y verbos
            content = self._correct_work_issues(content)
            
            # Correcciones SOCIAL - verbos no naturales
            content = self._correct_social_verbs(content)
            
            # Correcciones STACKING - verbos no naturales
            content = self._correct_stacking_verbs(content)
            
            # Guardar cambios
            if content != original:
                backup_path = file_path + '.final_backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return {
                    'success': True,
                    'corrections': len(self.corrections_applied),
                    'backup': backup_path,
                    'details': self.corrections_applied
                }
            else:
                return {
                    'success': True,
                    'corrections': 0,
                    'message': 'No corrections needed'
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _correct_method_verbs(self, content: str) -> str:
        """Corrige verbos no naturales en METHOD"""
        corrections = {
            'modela': 'opera',
            'rota': 'calcula',
            'bifurca': 'estructura',
            'simula': 'define',
            'proyecta': 'formaliza'
        }
        
        for old_verb, new_verb in corrections.items():
            pattern = f'(METHOD <[^>]+>\\s*=><=\\s*\\.\\.\\s*){old_verb}'
            if re.search(pattern, content):
                content = re.sub(pattern, f'\\1{new_verb}', content)
                self.corrections_applied.append(f"METHOD: {old_verb} → {new_verb}")
        
        return content
    
    def _correct_work_issues(self, content: str) -> str:
        """Corrige sujetos y verbos en WORK"""
        # Corregir sujetos
        subject_corrections = {
            'WORK {door}': 'WORK {door-afternoon}',
            'WORK {brake}': 'WORK {actuator}'
        }
        
        for old_subject, new_subject in subject_corrections.items():
            if old_subject in content:
                content = content.replace(old_subject, new_subject)
                self.corrections_applied.append(f"WORK subject: {old_subject} → {new_subject}")
        
        # Corregir verbos
        verb_corrections = {
            'abre': 'materializa',
            'cierra': 'detiene',
            'procesa': 'ejecuta',
            'verifica': 'custodia'
        }
        
        for old_verb, new_verb in verb_corrections.items():
            pattern = f'(WORK \\{{[^}}]+\\}}\\s*=><=\\s*\\.\\.\\s*){old_verb}'
            if re.search(pattern, content):
                content = re.sub(pattern, f'\\1{new_verb}', content)
                self.corrections_applied.append(f"WORK verb: {old_verb} → {new_verb}")
        
        return content
    
    def _correct_social_verbs(self, content: str) -> str:
        """Corrige verbos no naturales en SOCIAL"""
        corrections = {
            'planifica': 'distribuye',
            'activa': 'lanza',
            'estructura': 'organiza',
            'organiza': 'registra',
            'modela': 'filtra'
        }
        
        for old_verb, new_verb in corrections.items():
            pattern = f'(SOCIAL \\{{[^}}]+\\}}\\s*=><=\\s*\\.\\.\\s*){old_verb}'
            if re.search(pattern, content):
                content = re.sub(pattern, f'\\1{new_verb}', content)
                self.corrections_applied.append(f"SOCIAL: {old_verb} → {new_verb}")
        
        return content
    
    def _correct_stacking_verbs(self, content: str) -> str:
        """Corrige verbos no naturales en STACKING"""
        corrections = {
            'aquieta': 'cristaliza',
            'organiza': 'inmutabiliza',
            'estructura': 'preserva',
            'activa': 'archiva',
            'planifica': 'sella'
        }
        
        for old_verb, new_verb in corrections.items():
            pattern = f'(STACKING UF\\[H\\d+\\]\\s*=><=\\s*\\.\\.\\s*){old_verb}'
            if re.search(pattern, content):
                content = re.sub(pattern, f'\\1{new_verb}', content)
                self.corrections_applied.append(f"STACKING: {old_verb} → {new_verb}")
        
        return content
    
    def validate_final_results(self, file_path: str) -> Dict:
        """Valida resultados finales"""
        try:
            import sys
            imv_path = "/media/Personal/PLANERAI/DIRIME/IMV"
            if imv_path not in sys.path:
                sys.path.insert(0, imv_path)
            
            from core.grammar import validate
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraer prompts
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
                        'valid': result.result.value == 'VALID',
                        'warnings': len(result.warnings) if hasattr(result, 'warnings') else 0,
                        'errors': len(result.errors) if hasattr(result, 'errors') else 0,
                        'library': result.library.value if hasattr(result, 'library') else 'UNKNOWN',
                        'summary': result.summary() if hasattr(result, 'summary') else ''
                    })
                except Exception as e:
                    validation_results.append({
                        'index': i + 1,
                        'valid': False,
                        'warnings': 0,
                        'errors': 1,
                        'library': 'ERROR',
                        'summary': str(e)
                    })
            
            # Estadísticas finales
            total = len(validation_results)
            valid = sum(1 for r in validation_results if r['valid'])
            total_warnings = sum(r['warnings'] for r in validation_results)
            total_errors = sum(r['errors'] for r in validation_results)
            success_rate = (valid / total) * 100 if total > 0 else 0
            
            # Prompts restantes con warnings
            remaining_issues = [
                r for r in validation_results 
                if r['warnings'] > 0 or r['errors'] > 0
            ]
            
            return {
                'total_prompts': total,
                'valid_prompts': valid,
                'invalid_prompts': total - valid,
                'total_warnings': total_warnings,
                'total_errors': total_errors,
                'success_rate': success_rate,
                'remaining_issues': len(remaining_issues),
                'validation_results': validation_results,
                'ready_to_proceed': success_rate >= 90 and total_errors == 0
            }
            
        except Exception as e:
            return {'error': str(e), 'ready_to_proceed': False}

def main():
    """Función principal"""
    corrector = FinalPriorityCorrector()
    
    target_file = "/media/Personal/PLANERAI/DIRIME/OPTIMIZACION DE PROMPTS  para Windsurf/$thu 19-03 to $wed 25-03_optimizar para prompts WINDSUF.txt"
    
    print("🔧 APLICANDO CORRECCIONES FINALES PRIORITARIAS")
    print("=" * 70)
    
    if not os.path.exists(target_file):
        print(f"❌ Archivo no encontrado: {target_file}")
        return
    
    # Aplicar correcciones
    print(f"📁 Procesando: {target_file}")
    result = corrector.apply_all_corrections(target_file)
    
    if result['success']:
        corrections = result['corrections']
        print(f"✅ Correcciones aplicadas: {corrections}")
        
        if corrections > 0:
            print(f"📋 Backup creado: {result['backup']}")
            print("\n🔧 Detalles de correcciones:")
            for detail in result['details']:
                print(f"   • {detail}")
        
        # Validación final
        print("\n📊 VALIDACIÓN FINAL")
        print("-" * 40)
        validation = corrector.validate_final_results(target_file)
        
        if 'error' not in validation:
            print(f"📈 Total prompts: {validation['total_prompts']}")
            print(f"✅ Prompts válidos: {validation['valid_prompts']}")
            print(f"⚠️  Warnings restantes: {validation['total_warnings']}")
            print(f"❌ Errors restantes: {validation['total_errors']}")
            print(f"📊 Tasa de éxito: {validation['success_rate']:.1f}%")
            print(f"🔧 Issues restantes: {validation['remaining_issues']}")
            
            # Veredicto final
            if validation['ready_to_proceed']:
                print("\n🚀 ¡CORRECCIONES COMPLETADAS - SEGURO PROCEDER!")
                print("✅ Sistema listo para deployment")
            elif validation['success_rate'] >= 80:
                print("\n⚠️  CORRECCIONES ACEPTABLES - PROCEDER CON CUIDADO")
                print("📋 Revisar manualmente los warnings restantes")
            else:
                print("\n❌ CORRECCIONES INSUFICIENTES - REVISAR MANUALMENTE")
                print("🔧 Se requiere intervención manual adicional")
                
            # Mostrar ejemplos de issues restantes
            if validation['remaining_issues'] > 0:
                print(f"\n📋 Ejemplos de issues restantes (primeros 3):")
                remaining = [
                    r for r in validation['validation_results'] 
                    if r['warnings'] > 0 or r['errors'] > 0
                ][:3]
                for issue in remaining:
                    print(f"   Línea {issue['index']}: {issue['warnings']}W/{issue['errors']}E")
        else:
            print(f"❌ Error en validación: {validation['error']}")
    else:
        print(f"❌ Error aplicando correcciones: {result['error']}")

if __name__ == "__main__":
    main()
