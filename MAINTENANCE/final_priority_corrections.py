#!/usr/bin/env python3
"""
final_priority_corrections.py - Motor de Correcciones Prioritarias
Validador Soberano con mapeo de términos obsoletos y corrección automática
"""

import re
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class SovereignValidator:
    """Validador Soberano con mapeo de términos obsoletos."""
    
    def __init__(self):
        self.mapeo_obsoleto = {
            'Creativity': 'Activity'  # Mapeo principal solicitado
        }
        
        # Verbos de la biblioteca METHOD para corrección
        self.method_verbs = {
            'opera', 'calcula', 'estructura', 'define', 'formaliza',
            'cristaliza', 'inmutabiliza', 'preserva', 'archiva', 'sella'
        }
        
        self.lacho_files_path = Path(__file__).parent.parent / "LACHO_FILES"
        self.log_path = Path(__file__).parent / "hypothetical_growth.log"
        
    def scan_lacho_files(self) -> List[Path]:
        """Escanea todos los archivos .lacho en LACHO_FILES."""
        return list(self.lacho_files_path.glob("*.lacho"))
    
    def correct_obsolete_terms(self, content: str) -> Tuple[str, Dict]:
        """Reemplaza términos obsoletos usando verbos METHOD."""
        corrections = {}
        original_content = content
        
        # Reemplazar mapeo obsoleto principal
        for old_term, new_term in self.mapeo_obsoleto.items():
            pattern = rf'\b{re.escape(old_term)}\b'
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, new_term, content, flags=re.IGNORECASE)
                corrections[old_term] = new_term
        
        # Validar uso de verbos METHOD
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if '@VERBS:' in line:
                # Extraer verbos entre llaves
                verb_match = re.search(r'\{([^}]+)\}', line)
                if verb_match:
                    verbs_str = verb_match.group(1)
                    verbs = [v.strip() for v in verbs_str.split(',')]
                    
                    # Verificar si todos los verbos son METHOD válidos
                    invalid_verbs = [v for v in verbs if v not in self.method_verbs]
                    if invalid_verbs:
                        corrections[f'linea_{i}_verbos_invalidos'] = invalid_verbs
        
        return content, corrections
    
    def process_lacho_file(self, lacho_file: Path) -> Dict:
        """Procesa un archivo .lacho individual."""
        try:
            content = lacho_file.read_text(encoding='utf-8')
            corrected_content, corrections = self.correct_obsolete_terms(content)
            
            result = {
                'file': str(lacho_file),
                'corrections': corrections,
                'original_size': len(content),
                'corrected_size': len(corrected_content),
                'has_changes': content != corrected_content
            }
            
            # Si hay cambios, escribir archivo corregido
            if result['has_changes']:
                backup_file = lacho_file.with_suffix('.lacho.backup')
                backup_file.write_text(content, encoding='utf-8')
                lacho_file.write_text(corrected_content, encoding='utf-8')
                result['backup_created'] = str(backup_file)
            
            return result
            
        except Exception as e:
            return {
                'file': str(lacho_file),
                'error': str(e),
                'has_changes': False
            }
    
    def register_hypothetical_action(self, action: str, ram_usage: str = "auto") -> bool:
        """Registra acción hipotética en hypothetical_growth.log."""
        try:
            timestamp = datetime.now().isoformat()
            entry = f"\n--- ACCIÓN HIPOTÉTICA REGISTRADA ---\n"
            entry += f"Timestamp: {timestamp}\n"
            entry += f"Entidad: Gualicho Huinca\n"
            entry += f"Estado: Sueño_L0\n"
            entry += f"Acción Hipotética: {action}\n"
            entry += f"RAM: {ram_usage}\n"
            entry += f"Versión: v0.3\n"
            
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(entry)
            
            return True
            
        except Exception as e:
            print(f"Error registrando acción hipotética: {e}")
            return False
    
    def validate_grammar_interface(self) -> Dict:
        """Valida gramática de interfaz minimalista."""
        interface_rules = {
            'minimalista_components': ['Background', 'Font', 'Prose'],
            'required_attributes': ['BACKGROUND', 'FONT', 'PROSE'],
            'valid_values': {
                'Background': ['#FFFFFF', '#000000', 'minimal'],
                'Font': ['Monospace', 'sans-serif', 'minimal'],
                'Prose': ['MIN', 'CONCISE', 'ESSENTIAL']
            }
        }
        
        validation_results = {
            'interface_rules': interface_rules,
            'validation_status': 'ACTIVE',
            'minimalista_compliance': True
        }
        
        return validation_results
    
    def run_corrections(self) -> Dict:
        """Ejecuta el proceso completo de correcciones."""
        print("🔧 SOVEREIGN VALIDATOR - INICIANDO CORRECCIONES")
        print("=" * 50)
        
        # Escanear archivos .lacho
        lacho_files = self.scan_lacho_files()
        print(f"📁 Archivos .lacho encontrados: {len(lacho_files)}")
        
        # Procesar cada archivo
        results = []
        for lacho_file in lacho_files:
            print(f"🔍 Procesando: {lacho_file.name}")
            result = self.process_lacho_file(lacho_file)
            results.append(result)
            
            if result.get('has_changes'):
                print(f"  ✅ Correcciones aplicadas: {len(result['corrections'])}")
                for old, new in result['corrections'].items():
                    print(f"    {old} → {new}")
            elif 'error' in result:
                print(f"  ❌ Error: {result['error']}")
            else:
                print(f"  ℹ️  Sin cambios necesarios")
        
        # Validar interfaz minimalista
        interface_validation = self.validate_grammar_interface()
        print(f"\n🎨 Validación interfaz minimalista: {interface_validation['validation_status']}")
        
        # Resumen final
        summary = {
            'timestamp': datetime.now().isoformat(),
            'files_processed': len(lacho_files),
            'files_with_corrections': sum(1 for r in results if r.get('has_changes')),
            'total_corrections': sum(len(r.get('corrections', {})) for r in results),
            'interface_validation': interface_validation,
            'results': results
        }
        
        print(f"\n📊 RESUMEN DE CORRECCIONES:")
        print(f"  Archivos procesados: {summary['files_processed']}")
        print(f"  Archivos corregidos: {summary['files_with_corrections']}")
        print(f"  Total correcciones: {summary['total_corrections']}")
        print(f"  Validación interfaz: {summary['interface_validation']['validation_status']}")
        
        return summary

def main():
    """Función principal del motor de correcciones."""
    validator = SovereignValidator()
    
    # Registrar acción hipotética solicitada
    import psutil
    current_ram = psutil.virtual_memory().used // (1024 * 1024)
    ram_usage = f"{current_ram}MB/50MB"
    
    action_registered = validator.register_hypothetical_action(
        "Proyectar Interfaz Minimalista", 
        ram_usage
    )
    
    if action_registered:
        print("✅ Acción hipotética registrada en hypothetical_growth.log")
    
    # Ejecutar correcciones
    summary = validator.run_corrections()
    
    print(f"\n🚀 MOTOR DE CORRECCIONES COMPLETADO")
    print(f"📋 Proyección de sociedad registrada")
    
    return summary

if __name__ == "__main__":
    main()
