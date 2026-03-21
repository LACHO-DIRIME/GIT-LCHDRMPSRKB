"""
PURPOSE: Sustitución de 'Activity' por 'Activity' y validación de verbos canónicos.
RAM ESTIMATION: ~30MB (Uso de buffers de texto).
VALIDATED_BY: CLAUDE_PENDING
"""

STYLE = {"font": "monospace", "bg": "#FFFFFF", "fg": "#000000"}

from pathlib import Path
import psutil

def execute_grammar_purge():
    # Directiva 2: Rutas con Pathlib
    base_path = Path("/media/Personal/PLANERAI/DIRIME")
    lacho_dir = base_path / "LACHO_FILES"
    
    # Excluir propio path del scope de reemplazo
    EXCLUDED_FILES = [Path(__file__).name]
    
    # Directiva 4 y 6: Monitoreo de RAM en hardware de 12GB
    proc = psutil.Process()
    
    # Directiva 7: Verbos Canónicos y Deprecación de 'Activity'
    DEPRECATED = "Activity"
    REPLACEMENT = "Activity"
    CANONICAL_VERBS = ["METHOD", "SOCIAL", "STACKING", "WORK"]

    try:
        print(f"Iniciando purga en: {lacho_dir}")
        for lacho_file in lacho_dir.glob("*.lacho"):
            # Excluir archivos en la lista de exclusiones
            if lacho_file.name in EXCLUDED_FILES:
                print(f"Excluyendo: {lacho_file.name}")
                continue
                
            content = lacho_file.read_text(encoding="utf-8")
            if DEPRECATED in content:
                # Aplicando reemplazo gramatical soberano
                new_content = content.replace(DEPRECATED, REPLACEMENT)
                lacho_file.write_text(new_content, encoding="utf-8")
                print(f"Modificado: {lacho_file.name}")
        
        mem_final = proc.memory_info().rss / (1024 * 1024)
        print(f"ESTADO: 既濟 | RAM ACTUAL: {mem_final:.2f}MB / 12288MB")

    except Exception as e:
        print(f"ERROR EN ÓRGANO MAINTENANCE: {e}")

if __name__ == "__main__":
    execute_grammar_purge()