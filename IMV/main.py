#!/usr/bin/env python3
"""
DIRIME IMV — Implementación Mínima Verificable
Sistema soberano de validación LACHO con análisis Behavioral RAG.
"""

import argparse
import sys
import subprocess
import time
from typing import Optional

# ── Importaciones soberanas ─────────────────────────────────────────────
from core.grammar import validate
from core.samu import audit, get_status, get_scalar_s
from interface.chat import chat, get_summary
from core.ledger import (
    record_grammar, get_stats, verify_ledger,
    get_verb_frequency, get_library_stats, get_knot_distribution,
    get_session_timeline, export_crystals_report
)
from core.foundation import init_config_defaults, verify_sovereign_conditions

# Scheduler OS — integración soberana
try:
    import sys as _sys
    _sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent / "DIRIME_v2"))
    from scheduler.scheduler import rise, set_dia, estado_semana, planifica, DiaSoberano
    _SCHEDULER_ACTIVE = True
except Exception:
    _SCHEDULER_ACTIVE = False


# ── Sistema soberano principal ─────────────────────────────────────────
class SovereignSystem:
    """Sistema DIRIME IMV soberano."""
    
    def __init__(self):
        self.running = True
        self._initialize_system()

    def _initialize_system(self) -> None:
        """Inicialización soberana del sistema."""
        print("🔧 Inicializando DIRIME IMV...")
        
        # Iniciar Ollama si no está corriendo
        try:
            import httpx
            response = httpx.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code != 200:
                raise Exception()
        except:
            print("🚀 Iniciando Ollama local...")
            import subprocess
            subprocess.Popen(["ollama", "serve"], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
            import time
            time.sleep(3)  # Esperar a que inicie
        
        # Inicializar configuración por defecto
        init_config_defaults()
        
        # IME Modo RAG — CORPUS + Behavioral RAG
        try:
            from core.rag import build_full_index
            corpus_n, brag_n = build_full_index()
            if corpus_n > 0:
                # Distinguir CORPUS vs LIBRO vs CAPA 4
                from core.rag import _rag
                corpus_docs = sum(1 for d in _rag._docs if d.get("source","corpus")=="corpus")
                libro_docs = sum(1 for d in _rag._docs if d.get("source")=="libro")
                theater_docs = sum(1 for d in _rag._docs if d.get("source")=="theater")
                runner_docs = sum(1 for d in _rag._docs if d.get("source")=="runner")
                agent_docs = sum(1 for d in _rag._docs if d.get("source")=="agent")
                print(f"✅ IME RAG — {corpus_docs} CORPUS · {libro_docs} LIBRO · {theater_docs} THEATER · {runner_docs} RUNNER · {agent_docs} AGENT · {brag_n} patrones")
            else:
                print("⚠️  IME RAG — CORPUS vacío o no encontrado")
        except Exception:
            pass
        
        # SAMU #rise — activar período soberano del día
        try:
            import sys as _sys
            _scheduler_path = Path(__file__).parent.parent / "DIRIME_v2" / "scheduler"
            if _scheduler_path.exists():
                _sys.path.insert(0, str(_scheduler_path.parent.parent))
                from DIRIME_v2.scheduler.scheduler import rise, DiaSoberano
                rise_msg = rise()
                print(f"🌅 {rise_msg}")
        except Exception:
            pass  # scheduler es opcional
        
        # Verificar condiciones soberanas
        try:
            verify_sovereign_conditions("main")
            print("✅ Condiciones soberanas verificadas")
        except Exception as e:
            print(f"❌ Error en condiciones soberanas: {e}")
            sys.exit(1)
        
        # Verificar integridad del ledger
        if verify_ledger():
            print("✅ HL FABRIC ledger integro")
        else:
            print("⚠️ HL FABRIC ledger necesita atención")
        
        print("🚀 Sistema DIRIME IMV listo")

        # Scheduler OS — #rise automático al arranque
        if _SCHEDULER_ACTIVE:
            try:
                msg = rise()
                stats_s = estado_semana()
                dia_hoy = __import__('datetime').datetime.now().strftime('%A').lower()[:3]
                _dia_map = {'mon':'$mon','tue':'$tue','wed':'$wed','thu':'$thu',
                            'fri':'$fri','sat':'$sat','sun':'$sun'}
                dia_key = _dia_map.get(dia_hoy, '$mon')
                info = stats_s.get(dia_key, {})
                total = info.get('total', 0)
                resueltas = info.get('resueltas', 0)
                print(f"📅 {msg}")
                print(f"   {dia_key} — {resueltas}/{total} tareas soberanas")
            except Exception:
                pass  # scheduler falla silencioso — no bloquea arranque

    def interactive_mode(self) -> None:
        """Modo interactivo soberano."""
        print("\n" + "="*60)
        print("DIRIME IMV — MODO INTERACTIVO SOBERANO")
        print("Escribe 'help' para ayuda, 'quit' para salir")
        print("="*60)
        
        while self.running:
            try:
                user_input = input("\n👤 DIRIME> ").strip()
                
                if user_input.lower() in ["quit", "exit", "salir"]:
                    print("👋 Cerrando DIRIME IMV soberanamente")
                    self.running = False
                    continue
                
                if not user_input:
                    continue
                
                # Procesar mensaje a través del chat
                message = chat(user_input)
                
                print(f"\n⏱️  {message.processing_time_ms}ms | ✅ {message.sovereign_verified}")
                print(f"🤖 {message.response_content}")
                
                # Comandos especiales
                if user_input.lower() in ["verbos", "verbs"]:
                    self._show_verb_frequency()

                elif user_input.lower() in ["bibliotecas", "libs"]:
                    self._show_library_stats()

                elif user_input.lower() in ["nudos", "knots"]:
                    self._show_knot_distribution()

                elif user_input.lower() in ["timeline", "dias"]:
                    self._show_timeline()

                elif user_input.lower() in ["cristales", "crystals", "cr"]:
                    self._show_crystals_report()

                elif user_input.lower() in ["db", "ledger"]:
                    self._show_db_info()

                elif user_input.lower() in ["sched", "schedule", "semana"]:
                    self._show_scheduler()

                elif user_input.lower() in ["asks", "autoresearch", "diagnose"]:
                    self._run_autoresearch()

                elif user_input.lower() in ["notaria", "not", "actos"]:
                    self._show_notaria_status()

                elif user_input.lower().startswith("planifica "):
                    titulo = user_input[10:].strip()
                    if titulo and _SCHEDULER_ACTIVE:
                        t = planifica(titulo)
                        print(f"📅 Tarea planificada: {t.titulo} — {t.ref_soberana()}")
                    else:
                        print("⚠️  Scheduler no activo o título vacío")

                elif user_input.lower() in ["#set", "set_dia"]:
                    if _SCHEDULER_ACTIVE:
                        print(f"📅 {set_dia()}")
                    else:
                        print("⚠️  Scheduler no activo")
                
            except KeyboardInterrupt:
                print("\n👋 Interrupción detectada — cerrando soberanamente")
                self.running = False
            except EOFError:
                print("\n👋 EOF detectado — cerrando soberanamente")
                self.running = False
            except Exception as e:
                print(f"\n❌ Error: {e}")

    def _show_verb_frequency(self) -> None:
        """Muestra frecuencia de verbos — Behavioral RAG visible."""
        from core.ledger import get_verb_frequency, get_stats
        stats = get_stats()
        verbos = get_verb_frequency(25)
        threshold = 10

        lines = [
            "",
            "📊 **VERBOS SOBERANOS — FRECUENCIA VALID**",
            "",
            f"{'Verbo':<20} {'Usos':>6}  {'Estado':>15}",
            "─" * 48,
        ]
        for v in verbos:
            verb = v['verb']
            freq = v['freq']
            if freq >= threshold:
                estado = "✨ CRISTAL"
            elif freq >= threshold - 2:
                estado = f"⚡ falta {threshold-freq}"
            elif freq >= threshold - 5:
                estado = f"→ falta {threshold-freq}"
            else:
                estado = f"  falta {threshold-freq}"
            lines.append(f"  {verb:<18} {freq:>6}  {estado:>15}")

        lines += [
            "─" * 48,
            f"  Umbral de cristalización: {threshold} usos VALID",
            "",
        ]
        print("\n".join(lines))

    def _show_library_stats(self) -> None:
        """Muestra distribución de uso por biblioteca."""
        from core.ledger import get_library_stats
        libs = get_library_stats()

        lines = [
            "",
            "📚 **DISTRIBUCIÓN POR BIBLIOTECA**",
            "",
            f"{'Biblioteca':<12} {'Total':>7} {'VALID':>7} {'Precisión':>10}",
            "─" * 42,
        ]
        for l in libs:
            bar = "█" * int(l['precision'] / 10)
            lines.append(
                f"  {l['library']:<10} {l['total']:>7} "
                f"{l['valid']:>7} {l['precision']:>8}%  {bar}"
            )
        lines.append("")
        print("\n".join(lines))

    def _show_knot_distribution(self) -> None:
        """Muestra distribución de nudos usados."""
        from core.ledger import get_knot_distribution
        nudos = get_knot_distribution()
        total = sum(n['freq'] for n in nudos)

        lines = [
            "",
            "🪢 **DISTRIBUCIÓN DE NUDOS SOBERANOS**",
            "",
        ]
        for n in nudos:
            pct = round(n['freq'] / total * 100, 1) if total > 0 else 0
            bar = "█" * int(pct / 5)
            lines.append(f"  {n['knot']:<20} {n['freq']:>5}  {pct:>5}%  {bar}")
        lines.append("")
        print("\n".join(lines))

    def _show_timeline(self) -> None:
        """Muestra actividad soberana de los últimos 7 días."""
        from core.ledger import get_session_timeline
        dias = get_session_timeline(7)

        lines = [
            "",
            "📅 **TIMELINE SOBERANO — 7 DÍAS**",
            "",
            f"{'Día':<12} {'Total':>7} {'VALID':>7} {'Precisión':>10}",
            "─" * 42,
        ]
        for d in dias:
            bar = "█" * int(d['precision'] / 10)
            lines.append(
                f"  {d['day']:<10} {d['total']:>7} "
                f"{d['valid']:>7} {d['precision']:>8}%  {bar}"
            )
        if not dias:
            lines.append("  Sin actividad en los últimos 7 días.")
        lines.append("")
        print("\n".join(lines))

    def _show_crystals_report(self) -> None:
        """Reporte completo de cristales + verbos cerca del umbral."""
        from core.ledger import export_crystals_report
        report = export_crystals_report()
        crystals = report.get("crystals", [])
        near = report.get("near_threshold", [])

        lines = [
            "",
            f"✨ **CRISTALES SOBERANOS ACTIVOS — {len(crystals)} total**",
            "",
        ]
        for c in crystals:
            form = c['form'].replace("verbo_soberano:", "")
            lines.append(f"  {c['freq']:>4}x  {form}")

        if near:
            lines += [
                "",
                f"⚡ **VERBOS CERCA DEL UMBRAL ({len(near)} verbos)**",
                "",
            ]
            for n in near:
                lines.append(
                    f"  {n['freq']:>4}x  {n['verb']}  "
                    f"(faltan {n['falta']} para cristal)"
                )
        lines.append("")
        print("\n".join(lines))

    def _show_db_info(self) -> None:
        """Info técnica del ledger soberano."""
        from core.ledger import get_stats, verify_ledger
        from core.samu import get_scalar_s
        stats = get_stats()
        integrity = verify_ledger()

        lines = [
            "",
            "🗄️  **LEDGER SOBERANO — INFO DB**",
            "",
            f"  Path        : {stats.get('db_path', 'desconocido')}",
            f"  Estado      : {stats.get('status', '?')}",
            f"  Integridad  : {'✅ OK' if integrity else '❌ CORRUPTED'}",
            f"  Transac.    : {stats.get('transactions_total', 0)}",
            f"  Cristales   : {stats.get('crystals_total', 0)}",
            f"  Scalar S    : {get_scalar_s()}",
            "",
        ]
        print("\n".join(lines))

    def _show_notaria_status(self) -> None:
        from core.ledger import get_stats
        from core.samu import get_scalar_s
        stats      = get_stats()
        scalar     = get_scalar_s()
        tx         = stats.get("transactions_total", 0)
        THRESH_WU  = 0.78
        THRESH_H63 = 0.90
        filled     = int(scalar / THRESH_H63 * 20)
        bar        = "█" * min(filled, 20) + "░" * (20 - min(filled, 20))
        estado     = ("H63 既濟 ✅" if scalar >= THRESH_H63 else
                      "WU válido ⚡" if scalar >= THRESH_WU else
                      "KU pendiente ⏳")
        # intentar get_notaria_requirements si existe
        try:
            from core.ceo_alpha import get_notaria_requirements
            req = get_notaria_requirements()
            req_line = f"  CEO req     : H{req.get('hexagram','63')} · min_S={req.get('min_scalar',0.90)}"
        except Exception:
            req_line = "  CEO req     : H63 · min_S=0.90 (ceo_alpha pendiente)"
        lines = [
            "",
            "⊗  NOTARIA — ESTADO PIPELINE",
            "─" * 46,
            f"  Scalar S    : {scalar:.3f}  [{bar}]",
            f"  Estado      : {estado}",
            f"  TX total    : {tx}",
            req_line,
            "",
            "  PIPELINE:",
            "  N1 HEADCAT   grammar.validate()   ✅",
            "  N2 ELPULSAR  rag.suggest()        ✅",
            f"  N3 CHAIR_CEO S={scalar:.2f}             {'✅' if scalar >= THRESH_WU else '⚠️ '}",
            "  N4 DRONE     ledger.record()      ✅",
            "",
            "  PENDIENTES CAPA B:",
            "  ❌ IMV/core/ballpaper.py",
            "  ❌ /api/notaria/certifica · sella · inmutabiliza",
            "─" * 46,
        ]
        print("\n".join(lines))

    def _show_asks_status(self) -> None:
        """Muestra estado de Askings for autoresearching by technical horizons."""
        from pathlib import Path
        import json
        import yaml
        
        # Buscar en ambas ubicaciones posibles
        possible_dirs = [
            Path("/media/Personal/DIRIME/Askings for autoresearching by technical horizons"),
            Path(__file__).parent.parent / "Askings for autoresearching by technical horizons"
        ]
        
        asks_dir = None
        for dir_path in possible_dirs:
            if dir_path.exists():
                asks_dir = dir_path
                break
        
        if not asks_dir:
            print("❌ Directorio 'Askings for autoresearching by technical horizons' no encontrado")
            print("📍 Buscado en:")
            for dir_path in possible_dirs:
                print(f"   • {dir_path}")
            return
        
        lines = [
            "",
            "🔍 **ASKINGS FOR AUTORESEARCHING — TECHNICAL HORIZONS**",
            "",
        ]
        
        # Verificar archivos generados
        actual_structure = asks_dir / "actual_structure.json"
        sorted_upgrading = asks_dir / "sorted_upgrading.yml"
        gap_report = asks_dir / "gap_analysis_report.json"
        
        files_status = []
        if actual_structure.exists():
            files_status.append("✅ actual_structure.json")
        else:
            files_status.append("❌ actual_structure.json")
            
        if sorted_upgrading.exists():
            files_status.append("✅ sorted_upgrading.yml")
        else:
            files_status.append("❌ sorted_upgrading.yml")
            
        if gap_report.exists():
            files_status.append("✅ gap_analysis_report.json")
        else:
            files_status.append("❌ gap_analysis_report.json")
        
        lines.extend([
            "📁 Archivos generados:",
            f"   {'  '.join(files_status)}",
            "",
        ])
        
        # Mostrar resumen de actual_structure.json si existe
        if actual_structure.exists():
            try:
                with open(actual_structure, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                filesystem = data.get("filesystem", {})
                summary = filesystem.get("summary", {})
                
                lines.extend([
                    "📊 Estructura actual del repo:",
                    f"   Total módulos: {summary.get('total_modules', 0)}",
                    f"   Active: {summary.get('active', 0)}",
                    f"   Declared: {summary.get('declared', 0)}",
                    f"   Stub: {summary.get('stub', 0)}",
                    f"   Blocked: {summary.get('blocked', 0)}",
                    "",
                ])
                
                # Mostrar módulos bloqueados
                modules = filesystem.get("modules", {})
                blocked_modules = {k: v for k, v in modules.items() if v.get("status") == "blocked"}
                if blocked_modules:
                    lines.append("⚠️  Módulos bloqueados:")
                    for module, info in blocked_modules.items():
                        reason = info.get("reason", "unknown")
                        size = info.get("size_bytes", 0)
                        lines.append(f"   • {module} ({size} bytes) - {reason}")
                    lines.append("")
                
            except Exception as e:
                lines.append(f"❌ Error leyendo actual_structure.json: {e}")
                lines.append("")
        
        # Mostrar resumen de gap_analysis_report.json si existe
        if gap_report.exists():
            try:
                with open(gap_report, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                gap_analysis = data.get("gap_analysis", {})
                summary = gap_analysis.get("summary", {})
                
                lines.extend([
                    "🔍 Análisis de gaps:",
                    f"   Prioridad general: {summary.get('overall_priority', 'unknown').upper()}",
                    f"   Implementaciones faltantes: {summary.get('total_missing', 0)}",
                    f"   Módulos incompletos: {summary.get('total_incomplete', 0)}",
                    f"   Gaps de tests: {summary.get('total_test_gaps', 0)}",
                    f"   Gaps de dependencias: {summary.get('total_dependency_gaps', 0)}",
                    "",
                ])
                
                # Mostrar acciones inmediatas
                upgrade_plan = data.get("upgrade_plan", {})
                immediate = upgrade_plan.get("immediate_actions", [])
                if immediate:
                    lines.append("⚡ Acciones inmediatas:")
                    for action in immediate:
                        module = action.get("module", "unknown")
                        hours = action.get("estimated_hours", 0)
                        lines.append(f"   • {module} ({hours}h estimado)")
                    lines.append("")
                
            except Exception as e:
                lines.append(f"❌ Error leyendo gap_analysis_report.json: {e}")
                lines.append("")
        
        # Comandos sugeridos
        lines.extend([
            "🛠️  Comandos útiles:",
            "   cd ~/DIRIME && python3 tools/autoresearch_specs.py",
            "   cd ~/DIRIME && python3 tools/autoresearch_gap.py",
            "   cd ~/DIRIME/IMV && python3 main.py --asks",
            "",
        ])
        
        print("\n".join(lines))

    def _run_autoresearch(self) -> None:
        """Auto-diagnóstico soberano: specs → gap → asks."""
        import sys as _sys
        from pathlib import Path
        _sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
        try:
            import autoresearch_gap
            asks_path = autoresearch_gap.main()
            print(f"✅ asks generados: {asks_path.name}")
        except Exception as e:
            print(f"❌ autoresearch error: {e}")

    def _show_scheduler(self) -> None:
        """Muestra estado del Scheduler OS soberano."""
        if not _SCHEDULER_ACTIVE:
            print("⚠️  Scheduler OS no activo")
            return
        semana = estado_semana()
        print("\n📅 SCHEDULER OS — SEMANA SOBERANA")
        print("-" * 40)
        dias_orden = ["$mon","$tue","$wed","$thu","$fri","$sat","$sun"]
        for dia in dias_orden:
            info = semana.get(dia, {})
            total = info.get("total", 0)
            resueltas = info.get("resueltas", 0)
            if total == 0:
                print(f"  {dia}  —  sin tareas")
            else:
                barra = "█" * resueltas + "░" * (total - resueltas)
                print(f"  {dia}  [{barra}]  {resueltas}/{total}")
                for t in info.get("tareas", []):
                    estado_icon = "✅" if t["estado"] == "UF[H63]" else "⏳"
                    print(f"       {estado_icon} {t['titulo'][:45]}  {t.get('cluster','')}")
        print("-" * 40)

    def validate_mode(self, text: str) -> None:
        """Modo de validación directa."""
        print(f"🔍 Validando: {text}")
        
        parsed = validate(text)
        print(f"\n{parsed.summary()}")
        
        # LACHO_SCORE
        from core.grammar import lacho_score
        sc = lacho_score(parsed)
        bar = "█" * int(sc * 10) + "░" * (10 - int(sc * 10))
        print(f"  LACHO_SCORE [{bar}] {sc}")
        
        # Auditoría SAMU
        dispute = audit(parsed)
        if dispute:
            print(f"\n⚠️ SAMU detectó disputa: {dispute.description}")

    def stats_mode(self) -> None:
        """Modo de estadísticas."""
        print("📊 ESTADÍSTICAS DEL SISTEMA SOBERANO")
        print("-" * 40)
        
        # Estadísticas ledger
        from core.ledger import get_stats
        from core.samu import get_scalar_s
        stats = get_stats()
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        scalar = get_scalar_s()
        s_int = int(scalar * 20)
        s_bar = "█" * s_int + "░" * (20 - s_int)
        scalar_lines = [
            "",
            f"**Scalar S soberano**      : {scalar}",
            f"  [{s_bar}] {scalar * 100:.1f}%",
            "",
            "Referencia Scalar S:",
            "  ≥ 0.90 — coherencia soberana óptima",
            "  ≥ 0.70 — operativo soberanamente",
            "  < 0.70 — revisar disputas abiertas",
        ]
        print("\n".join(scalar_lines))
        
        print("-" * 40)
        
        # Estado SAMU
        print(f"Estado SAMU: {get_status()}")
        
        print("-" * 40)
        
        # Resumen chat
        summary = get_summary()
        print(f"Sesión chat: {summary}")


def main() -> None:
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="DIRIME IMV — Implementación Mínima Verificable",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py                    # modo interactivo
  python main.py --validate "TRUST FOUNDATION =><= .. verifica .. [scope] --[As de Guía] [term]"
  python main.py --stats            # estadísticas completas
  python main.py --verbos           # frecuencia de verbos VALID
  python main.py --cristales        # reporte cristales + verbos cerca umbral
  python main.py --bibliotecas      # distribución por biblioteca
  python main.py --nudos           # distribución de nudos
  python main.py --timeline         # actividad últimos 7 días
  python main.py --db              # info técnica ledger
  python main.py --sched           # estado semana soberana
  python main.py --asks            # Askings for autoresearching by technical horizons

Comandos en modo interactivo:
  verbos / verbs      Frecuencia de verbos VALID + distancia al cristal
  bibliotecas / libs  Distribución de uso por biblioteca
  nudos / knots       Distribución de nudos soberanos
  timeline / dias     Actividad soberana últimos 7 días
  cristales / cr      Reporte completo cristales + cerca del umbral
  db / ledger         Info técnica del ledger soberano
  help / ?           Ayuda completa del sistema
    """
    )
    
    parser.add_argument(
        "--validate", "-v",
        help="Validar sentencia LACHO directamente"
    )
    
    parser.add_argument(
        "--stats", "-s",
        action="store_true",
        help="Mostrar estadísticas del sistema"
    )
    
    parser.add_argument(
        "--version", action="version", version="DIRIME IMV 0.1.2"
    )
    
    parser.add_argument("--sched",
        action="store_true",
        help="Mostrar estado del Scheduler OS soberano")
    
    parser.add_argument("--asks", action="store_true",
                        help="Auto-diagnóstico soberano via Groq → genera $dia_asks")
    
    parser.add_argument("--notaria", action="store_true",
                      help="Estado del pipeline notarial soberano")
    
    args = parser.parse_args()
    
    # Inicializar sistema
    system = SovereignSystem()
    
    if args.validate:
        system.validate_mode(args.validate)
    elif args.stats:
        system.stats_mode()
    elif args.sched:
        system._show_scheduler()
    elif args.asks:
        system._run_autoresearch()
    elif args.notaria:
        system._show_notaria_status()
    else:
        system.interactive_mode()


if __name__ == "__main__":
    main()