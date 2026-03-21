#!/usr/bin/env python3
"""
Correcciones Prioritarias de Validación - Prompts LACHO
Corrige WARNINGs críticos encontrados en validación gramatical
"""

import os
import re
from typing import List, Dict, Tuple

class PromptValidatorCorrector:
    """Corrector de prompts LACHO basado en validación gramatical"""
    
    def __init__(self):
        self.corrections_applied = []
        self.validation_errors = []
        
    def correct_prompt(self, prompt: str) -> str:
        """Aplica correcciones automáticas a un prompt LACHO"""
        original = prompt
        corrected = prompt
        
        # Corrección 1: SOCIAL - verbos no naturales
        corrected = self._correct_social_verbs(corrected)
        
        # Corrección 2: STACKING - verbos no naturales  
        corrected = self._correct_stacking_verbs(corrected)
        
        # Corrección 3: WORK - sujetos no canónicos
        corrected = self._correct_work_subjects(corrected)
        
        # Corrección 4: WORK - verbos no naturales
        corrected = self._correct_work_verbs(corrected)
        
        if corrected != original:
            self.corrections_applied.append({
                'original': original,
                'corrected': corrected,
                'changes': self._detect_changes(original, corrected)
            })
            
        return corrected
    
    def _correct_social_verbs(self, prompt: str) -> str:
        """Corrige verbos no naturales para biblioteca SOCIAL"""
        social_verb_corrections = {
            'planifica': 'distribuye',
            'activa': 'lanza',
            'estructura': 'organiza',
            'organiza': 'registra',
            'modela': 'filtra'
        }
        
        # Buscar sentencias SOCIAL
        social_pattern = r'(SOCIAL \{[^}]+\}\s*=><=\s*\.\.\s*)(\w+)'
        
        def replace_social_verb(match):
            prefix = match.group(1)
            verb = match.group(2)
            corrected_verb = social_verb_corrections.get(verb, verb)
            return f"{prefix}{corrected_verb}"
        
        return re.sub(social_pattern, replace_social_verb, prompt)
    
    def _correct_stacking_verbs(self, prompt: str) -> str:
        """Corrige verbos no naturales para biblioteca STACKING"""
        stacking_verb_corrections = {
            'aquieta': 'cristaliza',
            'organiza': 'inmutabiliza',
            'estructura': 'preserva',
            'activa': 'archiva',
            'planifica': 'sella'
        }
        
        # Buscar sentencias STACKING
        stacking_pattern = r'(STACKING UF\[H\d+\]\s*=><=\s*\.\.\s*)(\w+)'
        
        def replace_stacking_verb(match):
            prefix = match.group(1)
            verb = match.group(2)
            corrected_verb = stacking_verb_corrections.get(verb, verb)
            return f"{prefix}{corrected_verb}"
        
        return re.sub(stacking_pattern, replace_stacking_verb, prompt)
    
    def _correct_work_subjects(self, prompt: str) -> str:
        """Corrige sujetos no canónicos para biblioteca WORK"""
        work_subject_corrections = {
            '{door}': '{door-afternoon}',
            '{brake}': '{actuator}',
            '{scheduler}': '{doorman-mobile}'
        }
        
        for old_subject, new_subject in work_subject_corrections.items():
            prompt = prompt.replace(old_subject, new_subject)
            
        return prompt
    
    def _correct_work_verbs(self, prompt: str) -> str:
        """Corrige verbos no naturales para biblioteca WORK"""
        work_verb_corrections = {
            'abre': 'materializa',
            'cierra': 'detiene',
            'procesa': 'ejecuta',
            'verifica': 'custodia',
            'analiza': 'sella'
        }
        
        # Buscar sentencias WORK
        work_pattern = r'(WORK \{[^}]+\}\s*=><=\s*\.\.\s*)(\w+)'
        
        def replace_work_verb(match):
            prefix = match.group(1)
            verb = match.group(2)
            corrected_verb = work_verb_corrections.get(verb, verb)
            return f"{prefix}{corrected_verb}"
        
        return re.sub(work_pattern, replace_work_verb, prompt)
    
    def _detect_changes(self, original: str, corrected: str) -> List[str]:
        """Detecta los cambios aplicados"""
        changes = []
        
        if 'planifica' in original and 'distribuye' in corrected:
            changes.append("planifica → distribuye (SOCIAL)")
        if 'aquieta' in original and 'cristaliza' in corrected:
            changes.append("aquieta → cristaliza (STACKING)")
        if '{door}' in original and '{door-afternoon}' in corrected:
            changes.append("{door} → {door-afternoon} (WORK)")
        if 'abre' in original and 'materializa' in corrected:
            changes.append("abre → materializa (WORK)")
            
        return changes
    
    def validate_corrected_prompt(self, prompt: str) -> Dict:
        """Valida un prompt corregido usando el validador de IMV"""
        try:
            import sys
            imv_path = "/media/Personal/PLANERAI/DIRIME/IMV"
            if imv_path not in sys.path:
                sys.path.insert(0, imv_path)
            
            from core.grammar import validate
            
            result = validate(prompt)
            
            return {
                'valid': result.result.value == 'VALID',
                'warnings': len(result.warnings) if hasattr(result, 'warnings') else 0,
                'errors': len(result.errors) if hasattr(result, 'errors') else 0,
                'library': result.library.value if hasattr(result, 'library') else 'UNKNOWN',
                'taxonomy': result.taxonomy.class_name if hasattr(result, 'taxonomy') else 'N/A',
                'summary': result.summary() if hasattr(result, 'summary') else 'No summary'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'warnings': 0,
                'errors': 1,
                'library': 'ERROR',
                'taxonomy': 'N/A',
                'summary': f'Error de validación: {e}'
            }
    
    def process_prompt_file(self, file_path: str) -> Dict:
        """Procesa un archivo de prompts completo"""
        results = {
            'file': file_path,
            'total_prompts': 0,
            'corrections_applied': 0,
            'validation_results': [],
            'summary': {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraer prompts LACHO (líneas que contienen =><=)
            prompts = []
            for line in content.split('\n'):
                if '=><= ..' in line and '--[' in line and '[term]' in line:
                    prompts.append(line.strip())
            
            results['total_prompts'] = len(prompts)
            
            # Procesar cada prompt
            for i, prompt in enumerate(prompts):
                # Corregir prompt
                corrected_prompt = self.correct_prompt(prompt)
                
                # Validar prompt corregido
                validation = self.validate_corrected_prompt(corrected_prompt)
                
                results['validation_results'].append({
                    'index': i + 1,
                    'original': prompt,
                    'corrected': corrected_prompt,
                    'validation': validation
                })
                
                if corrected_prompt != prompt:
                    results['corrections_applied'] += 1
            
            # Calcular resumen
            valid_count = sum(1 for r in results['validation_results'] if r['validation']['valid'])
            warning_count = sum(r['validation']['warnings'] for r in results['validation_results'])
            error_count = sum(r['validation']['errors'] for r in results['validation_results'])
            
            results['summary'] = {
                'valid_prompts': valid_count,
                'invalid_prompts': len(prompts) - valid_count,
                'total_warnings': warning_count,
                'total_errors': error_count,
                'success_rate': (valid_count / len(prompts)) * 100 if prompts else 0
            }
            
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def generate_correction_report(self, results: Dict) -> str:
        """Genera reporte de correcciones"""
        report = []
        report.append("# REPORTE DE CORRECCIONES PROMPTS LACHO")
        report.append("=" * 60)
        report.append(f"Archivo: {results['file']}")
        report.append(f"Total prompts: {results['total_prompts']}")
        report.append(f"Correcciones aplicadas: {results['corrections_applied']}")
        report.append("")
        
        if 'error' in results:
            report.append(f"ERROR: {results['error']}")
            return "\n".join(report)
        
        summary = results['summary']
        report.append("## RESUMEN DE VALIDACIÓN")
        report.append(f"- Prompts válidos: {summary['valid_prompts']}")
        report.append(f"- Prompts inválidos: {summary['invalid_prompts']}")
        report.append(f"- Warnings totales: {summary['total_warnings']}")
        report.append(f"- Errors totales: {summary['total_errors']}")
        report.append(f"- Tasa de éxito: {summary['success_rate']:.1f}%")
        report.append("")
        
        if self.corrections_applied:
            report.append("## CORRECCIONES APLICADAS")
            for i, correction in enumerate(self.corrections_applied, 1):
                report.append(f"### Corrección {i}")
                report.append(f"Cambios: {', '.join(correction['changes'])}")
                report.append(f"Original: {correction['original']}")
                report.append(f"Corregido: {correction['corrected']}")
                report.append("")
        
        report.append("## DETALLE DE VALIDACIÓN")
        for result in results['validation_results']:
            validation = result['validation']
            status = "✅" if validation['valid'] else "❌"
            report.append(f"{status} Prompt {result['index']}: {validation['library']}")
            if validation['warnings'] > 0:
                report.append(f"   ⚠️  {validation['warnings']} warnings")
            if validation['errors'] > 0:
                report.append(f"   ❌ {validation['errors']} errors")
            report.append("")
        
        return "\n".join(report)

def main():
    """Función principal de corrección"""
    corrector = PromptValidatorCorrector()
    
    # Archivo de prompts a corregir
    prompts_file = "/media/Personal/PLANERAI/DIRIME/OPTIMIZACION DE PROMPTS  para Windsurf/$thu 19-03 to $wed 25-03_optimizar para prompts WINDSUF.txt"
    
    print("🔧 CORRIGIENDO PROMPTS LACHO PRIORITARIOS")
    print("=" * 60)
    
    if os.path.exists(prompts_file):
        print(f"📁 Procesando: {prompts_file}")
        results = corrector.process_prompt_file(prompts_file)
        
        # Mostrar resumen
        summary = results.get('summary', {})
        print(f"📊 Total prompts: {results.get('total_prompts', 0)}")
        print(f"🔧 Correcciones aplicadas: {results.get('corrections_applied', 0)}")
        print(f"✅ Prompts válidos: {summary.get('valid_prompts', 0)}")
        print(f"⚠️  Warnings totales: {summary.get('total_warnings', 0)}")
        print(f"📈 Tasa de éxito: {summary.get('success_rate', 0):.1f}%")
        
        # Generar reporte
        report = corrector.generate_correction_report(results)
        report_file = "/media/Personal/PLANERAI/DIRIME/corrections_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📋 Reporte guardado en: {report_file}")
        
        # Verificar si es seguro proceder
        success_rate = summary.get('success_rate', 0)
        if success_rate >= 90:
            print("🚀 ¡Correcciones completadas - seguro proceder!")
        elif success_rate >= 80:
            print("⚠️  Correcciones aceptables - proceder con cuidado")
        else:
            print("❌ Demasiados errores - revisar manualmente")
            
    else:
        print(f"❌ Archivo no encontrado: {prompts_file}")

if __name__ == "__main__":
    main()
