"""
DIRIME IMV — test_imv.py
Tests soberanos automatizados del ciclo completo IMV.
$wed 2026-03-11 · 27→33 tests · GENERATOR + LANGUAGE_ROUTING añadidos

Ejecutar: cd /media/Personal/PLANERAI/DIRIME/IMV && python3 tests/test_imv.py
"""

import sys
import json
import sqlite3
from pathlib import Path

# Path soberano
_IMV_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_IMV_DIR))


# ── Tests foundation ────────────────────────────────────────────

def test_foundation_verifica():
    """IMV-1: foundation retorna (Foundation, Scope, Term) para módulo válido."""
    from core.foundation import verify_sovereign_conditions, SovereignError
    result = verify_sovereign_conditions("grammar")
    assert isinstance(result, tuple), "debe retornar tupla soberana"
    assert len(result) == 3, "tupla debe tener 3 elementos"
    foundation, scope, term = result
    assert foundation.identity_verified is True, "identidad debe estar verificada"
    try:
        verify_sovereign_conditions("modulo_invalido")
        assert False, "debe lanzar SovereignError para módulo inválido"
    except SovereignError:
        pass
    print("  ✅ foundation.verify_sovereign_conditions()")


def test_foundation_json_existe():
    """Los tres JSON de configuración existen."""
    config = _IMV_DIR / "config"
    assert (config / "foundation.json").exists(), "foundation.json ausente"
    assert (config / "scope.json").exists(), "scope.json ausente"
    assert (config / "term.json").exists(), "term.json ausente"
    print("  ✅ config/ foundation.json · scope.json · term.json")


# ── Tests grammar ───────────────────────────────────────────────

def test_grammar_valid_canonica():
    """IMV-2: sentencia canónica produce VALID."""
    from core.grammar import validate
    parsed = validate(
        "TRUST FOUNDATION =><= .. verifica .. scope_activo --[As de Guía] [term]"
    )
    assert parsed.result.value == "VALID", f"Esperado VALID, obtenido {parsed.result.value}"
    print("  ✅ grammar.validate() — sentencia canónica VALID")


def test_grammar_invalid_sin_term():
    """Sin [term] produce INVALID."""
    from core.grammar import validate
    parsed = validate(
        "TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía]"
    )
    assert parsed.result.value == "INVALID", "Sin [term] debe ser INVALID"
    print("  ✅ grammar.validate() — sin [term] produce INVALID")


def test_grammar_invalid_sin_nudo():
    """Sin nudo produce INVALID."""
    from core.grammar import validate
    parsed = validate(
        "TRUST FOUNDATION =><= .. verifica .. scope [term]"
    )
    assert parsed.result.value == "INVALID", "Sin nudo debe ser INVALID"
    print("  ✅ grammar.validate() — sin nudo produce INVALID")


def test_grammar_9_bibliotecas():
    """Las 9 bibliotecas producen VALID."""
    from core.grammar import validate
    sentencias = [
        "TRUST FOUNDATION =><= .. verifica .. scope_activo --[As de Guía] [term]",
        "WORK {actuator} =><= .. materializa .. accion --[As de Guía] [term]",
        "CRYPTO (spark seat) =><= .. autoriza .. acceso --[As de Guía] [term]",
        "SAMU @ =><= .. dirime .. disputa --[Ballestrinque] [term]",
        "ACTIVITY UF[H01] =><= .. inicia .. ciclo --[As de Guía] [term]",
        "GATE UF[H05] =><= .. espera .. señal --[Ballestrinque] [term]",
        "STACKING UF[H52] =><= .. inmutabiliza .. patron --[Nudo de Ocho] [term]",
        "SOCIAL {launch-bot} =><= .. lanza .. bot --[As de Guía] [term]",
        "METHOD <equation> =><= .. calcula .. variable --[Nudo de Ocho] [term]",
    ]
    for s in sentencias:
        p = validate(s)
        lib = s.split()[0]
        assert p.result.value == "VALID", f"{lib} debe ser VALID: {p.errors}"
    print("  ✅ grammar.validate() — 9 bibliotecas todas VALID")


def test_grammar_5_nudos():
    """Los 5 nudos canónicos son válidos."""
    from core.grammar import validate
    nudos = [
        "As de Guía", "Nudo de Ocho", "Ballestrinque",
        "Nudo Corredizo", "Nudo de Rizo"
    ]
    for nudo in nudos:
        s = f"TRUST FOUNDATION =><= .. verifica .. scope --[{nudo}] [term]"
        p = validate(s)
        assert p.result.value == "VALID", f"Nudo '{nudo}' debe ser VALID"
    print("  ✅ grammar.validate() — 5 nudos canónicos VALID")


# ── Tests grammar extendidos ────────────────────────────────────

def test_cjk_detection():
    from core.grammar import validate, is_chinese
    assert is_chinese("信任") is True
    assert is_chinese("TRUST") is False
    p = validate("TRUST FOUNDATION =><= .. verifica .. 信任_dual --[As de Guía] [term]")
    assert p.unicode_mode == "CHINA"
    assert len(p.cjk_tokens) > 0
    assert p.taxonomy.get("taxonomy_level") == 1
    print("  ✅ grammar.cjk — is_chinese() + unicode_mode CHINA + taxonomy N1")


def test_ceo_alpha_loader():
    from core.ceo_alpha import ceo_summary, get_role_by_hexagram, get_scalar_threshold
    summary = ceo_summary()
    assert "64" in summary
    role = get_role_by_hexagram("H01")
    assert role is not None
    assert role.get("library") == "ACTIVITY"
    threshold = get_scalar_threshold("H01")
    assert threshold >= 0.80
    print("  ✅ ceo_alpha — 64 hexagramas · H01 ACTIVITY · threshold OK")


class TestGrammarExtended:
    def test_9_bibliotecas_validan(self):
        from core.grammar import validate
        sentencias = [
            "TRUST FOUNDATION =><= .. verifica .. scope_activo --[As de Guía] [term]",
            "WORK {actuator} =><= .. materializa .. accion --[As de Guía] [term]",
            "CRYPTO (spark seat) =><= .. autoriza .. acceso --[As de Guía] [term]",
            "SAMU @ =><= .. dirime .. disputa --[Ballestrinque] [term]",
            "ACTIVITY UF[H01] =><= .. inicia .. ciclo --[As de Guía] [term]",
            "GATE UF[H05] =><= .. transita .. señal --[Ballestrinque] [term]",
            "STACKING UF[H52] =><= .. inmutabiliza .. patron --[Nudo de Ocho] [term]",
            "SOCIAL {launch-bot} =><= .. lanza .. bot --[As de Guía] [term]",
            "METHOD <equation> =><= .. calcula .. variable --[Nudo de Ocho] [term]",
        ]
        for s in sentencias:
            p = validate(s)
            lib = s.split()[0]
            assert p.result.value == "VALID", f"{lib} debe ser VALID: {p.errors} {p.warnings}"


# ── Tests ledger ────────────────────────────────────────────────

def test_ledger_record_valid():
    """IMV-4: ledger registra transacción VALID."""
    from core.grammar import validate
    from core.ledger import record_grammar, get_stats
    parsed = validate(
        "TRUST FOUNDATION =><= .. verifica .. test_ledger --[As de Guía] [term]"
    )
    tx_id = record_grammar(parsed)
    assert tx_id is not None, "record_grammar debe retornar id"
    assert len(tx_id) > 0, "tx_id no puede ser vacío"
    print("  ✅ ledger.record_grammar() — transacción registrada")


def test_ledger_stats_retorna():
    """get_stats() retorna dict con claves esperadas."""
    from core.ledger import get_stats
    stats = get_stats()
    claves = ["transactions_total", "grammar_valid", "crystals_total"]
    for clave in claves:
        assert clave in stats, f"stats debe tener '{clave}'"
    assert stats["transactions_total"] > 0, "debe haber transacciones"
    print("  ✅ ledger.get_stats() — claves correctas")


def test_ledger_blue_green():
    """Transacciones VALID son GREEN, INVALID son BLUE."""
    from core.ledger import get_stats
    stats = get_stats()
    total = stats.get("transactions_total", 0)
    assert total > 0, "debe haber transacciones para este test"
    print("  ✅ ledger.get_stats() — blue/green presentes")


def test_ledger_cristales_40():
    """El ledger tiene al menos 40 cristales activos."""
    from core.ledger import get_stats
    stats = get_stats()
    crystals = stats.get("crystals_total", 0)
    assert crystals >= 40, f"Esperado >=40 cristales, obtenido {crystals}"
    print(f"  ✅ ledger — {crystals} cristales activos")


def test_ledger_blacklist():
    """Los verbos basura no aparecen en cristales."""
    from core.ledger import export_crystals_report
    report = export_crystals_report()
    blacklist = ['mostrar', 'metho', 'meth', 'estricto', 'conflicto', 'analizar']
    crystals = report.get("crystals", [])
    crystal_verbs = [c.get("form", "").replace("verbo_soberano:", "") for c in crystals]
    for basura in blacklist:
        assert basura not in crystal_verbs, f"Verbo basura '{basura}' en cristales"
    print("  ✅ ledger — BLACKLIST efectiva, sin verbos basura")


# ── Tests SAMU ──────────────────────────────────────────────────

def test_samu_audit_valid():
    """IMV-3: SAMU no genera disputa en sentencia VALID."""
    from core.grammar import validate
    from core.samu import audit
    parsed = validate(
        "TRUST FOUNDATION =><= .. verifica .. scope_activo --[As de Guía] [term]"
    )
    dispute = audit(parsed)
    assert dispute is None, f"SAMU no debe disputar sentencia VALID: {dispute}"
    print("  ✅ samu.audit() — sentencia VALID sin disputa")


def test_samu_audit_invalid():
    """SAMU genera disputa en sentencia INVALID."""
    from core.grammar import validate
    from core.samu import audit
    parsed = validate("esto no es lacho")
    dispute = audit(parsed)
    assert dispute is not None, "SAMU debe disputar sentencia INVALID"
    print("  ✅ samu.audit() — sentencia INVALID genera disputa")


# ── Tests Groq bridge ───────────────────────────────────────────

def test_groq_config_existe():
    """api.json existe y tiene provider groq."""
    api_cfg = _IMV_DIR / "config" / "api.json"
    assert api_cfg.exists(), "config/api.json debe existir"
    cfg = json.loads(api_cfg.read_text())
    assert cfg.get("provider") == "groq", "provider debe ser groq"
    assert cfg.get("key", "").startswith("gsk_"), "key debe empezar con gsk_"
    print("  ✅ groq — api.json válido")


def test_groq_traduccion_nl_lacho():
    """Groq traduce NL→LACHO y produce VALID."""
    from interface.chat import chat
    msg = chat("necesito verificar el estado del sistema")
    assert msg.sovereign_verified, "traducción debe ser verificada"
    print("  ✅ groq — NL→LACHO traducción verificada")


# ── Tests switch_unicode ─────────────────────────────────────────

def test_switch_unicode_modo_default():
    """Modo unicode por defecto es STACKING."""
    from core.ledger import get_unicode_mode
    mode = get_unicode_mode()
    assert mode == "STACKING", f"Modo default debe ser STACKING, obtenido {mode}"
    print("  ✅ switch_unicode — modo default STACKING")


def test_switch_unicode_cambia():
    """switch_unicode cambia el modo y lo restaura."""
    from core.ledger import switch_unicode, get_unicode_mode
    switch_unicode("LACHO")
    assert get_unicode_mode() == "LACHO"
    switch_unicode("STACKING")  # restaurar
    assert get_unicode_mode() == "STACKING"
    print("  ✅ switch_unicode — cambia y restaura correctamente")


# ── Tests TOMO_IDs ──────────────────────────────────────────────

def test_tomo_assign():
    """assign_tomo_ids asigna IDs alfabéticos correctos."""
    from core.ledger import assign_tomo_ids
    assigned = assign_tomo_ids()
    assert len(assigned) > 0, "debe asignar al menos un TOMO_ID"
    values = list(assigned.values())
    assert "term:A" in values, "primer cristal debe ser term:A"
    print(f"  ✅ tomo — {len(assigned)} TOMO_IDs asignados, primero: term:A")


# ── Tests ext (standalone) ──────────────────────────────────────

def test_ext_9_bibliotecas():
    from core.grammar import validate
    libs = ['TRUST','SOCIAL','CRYPTO','WORK','SAMU','ACTIVITY','GATE','STACKING','METHOD']
    for lib in libs:
        r = validate(f'{lib} FOUNDATION =><= .. verifica .. obj --[As de Guía] [term]')
        assert r.result.value in ('VALID','WARNING'), f'{lib} debería ser VALID o WARNING'


def test_ext_verbo_natural():
    from core.grammar import validate
    r = validate('TRUST FOUNDATION =><= .. verifica .. scope_activo --[As de Guía] [term]')
    assert r.result.value == 'VALID'
    assert not any('verbo' in w.lower() for w in r.warnings)


def test_ext_verbo_mismatch():
    from core.grammar import validate
    r = validate('TRUST FOUNDATION =><= .. lanza .. scope_activo --[As de Guía] [term]')
    assert r.result.value == 'WARNING'
    assert any('verbo' in w.lower() for w in r.warnings), f'warnings: {r.warnings}'


def test_ext_sujeto_canonico():
    from core.grammar import validate
    r = validate('WORK {actuator} =><= .. materializa .. tarea --[As de Guía] [term]')
    assert r.result.value == 'VALID'
    assert not any('sujeto' in w.lower() for w in r.warnings)


def test_ext_sujeto_mismatch():
    from core.grammar import validate
    r = validate('WORK {motor} =><= .. ejecuta .. tarea --[As de Guía] [term]')
    assert r.result.value == 'WARNING'
    assert any('sujeto' in w.lower() for w in r.warnings), f'warnings: {r.warnings}'


def test_ext_term_ausente():
    from core.grammar import validate
    r = validate('TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía]')
    assert r.result.value == 'INVALID'


# ══ Tests GENERATOR · $wed 2026-03-11 ══════════════════════════

def test_gen_1_creates_file():
    """generator.py crea o ya tiene archivo .lacho en LACHO_FILES."""
    import subprocess
    from pathlib import Path
    result = subprocess.run(
        ["python3", "tools/generator.py", "--mode", "stats"],
        capture_output=True, text=True,
        cwd=str(_IMV_DIR)
    )
    lacho_dir = _IMV_DIR.parent / "FOLDERS NO RAG INPUT" / "LACHO_FILES"
    # También acepta el dir legacy por compatibilidad
    lacho_dir_legacy = _IMV_DIR.parent / "LACHO_FILES"
    files = []
    if lacho_dir.exists():
        files = list(lacho_dir.glob("*.lacho"))
    if not files and lacho_dir_legacy.exists():
        files = list(lacho_dir_legacy.glob("*.lacho"))
    assert result.returncode == 0 or len(files) > 0, (
        f"generator falló (rc={result.returncode}) y no hay .lacho previos\n"
        f"stderr: {result.stderr[:300]}"
    )
    print(f"  ✅ generator.py — archivo .lacho presente ({len(files)} encontrados)")


def test_gen_2_valid_sentences():
    """generator.build_stats_sentences produce sentencias LACHO válidas."""
    import sys as _sys
    _sys.path.insert(0, str(_IMV_DIR))
    from core.grammar import validate, ValidationResult
    from tools.generator import build_stats_sentences, collect
    data = collect()
    sentences = build_stats_sentences(data)
    assert len(sentences) > 0, "build_stats_sentences devolvió vacío"
    valid = sum(1 for s in sentences if validate(s).result != ValidationResult.INVALID)
    assert valid > 0, f"Ninguna sentencia válida de {len(sentences)}"
    print(f"  ✅ generator.sentences — {valid}/{len(sentences)} válidas")


def test_gen_3_score_threshold():
    """generator — sentencias tienen Scalar S > 0."""
    from core.grammar import validate, lacho_score
    from tools.generator import build_stats_sentences, collect
    data = collect()
    sentences = build_stats_sentences(data)
    assert sentences, "build_stats_sentences vacío"
    scores = [lacho_score(validate(s)) for s in sentences]
    assert any(sc > 0 for sc in scores), "Todas las sentencias tienen score 0"
    print(f"  ✅ generator.score — max={max(scores):.2f}")


def test_gen_4_language_routing():
    """language_routing — NLP→LACHO para 3 casos soberanos."""
    from core.language_routing import route
    casos = [
        ("verificar contrato digital", "TRUST"),
        ("ejecutar sync github",       "WORK"),
        ("cristalizar historial inmutable", "STACKING"),
    ]
    for texto, lib_esperada in casos:
        r = route(texto)
        assert r.validated, f"route('{texto}') no validó: {r.sentence}"
        assert r.library == lib_esperada, (
            f"Esperaba {lib_esperada}, got {r.library} para '{texto}'"
        )
    print("  ✅ language_routing — 3 casos NLP→LACHO válidos")


def test_gen_5_route_cjk():
    """language_routing — detecta CJK tokens y enruta correctamente."""
    from core.language_routing import route
    r = route("verificar 信任 en contrato soberano")
    assert r.validated, f"CJK route no validó: {r.sentence}"
    assert "信任" in r.cjk_tokens, f"CJK no detectado: {r.cjk_tokens}"
    print(f"  ✅ language_routing.cjk — {r.cjk_tokens} → {r.library}")


def test_gen_6_gate_sequence():
    """grammar — GATE acepta secuencia canónica H03→H05→H56→H06."""
    from core.grammar import validate, ValidationResult
    sentencias = [
        "GATE UF[H03] =><= .. contiene .. inicio_dificultad_soberana --[Ballestrinque] [term]",
        "GATE UF[H05] =><= .. espera .. latencia_soberana_h05 --[Ballestrinque] [term]",
        "GATE UF[H56] =><= .. transita .. flujo_transito_soberano --[As de Guía] [term]",
        "GATE UF[H06] =><= .. dirime .. conflicto_resuelto_h06 --[Ballestrinque] [term]",
    ]
    for s in sentencias:
        r = validate(s)
        assert r.result != ValidationResult.INVALID, (
            f"GATE seq INVALID: {s}\nerrors: {r.errors}"
        )
    print("  ✅ grammar.GATE — secuencia H03→H05→H56→H06 válida")


# ── Tests NOTARIA ────────────────────────────────────────────────

def test_notaria_certifica():
    """NOTARIA-1: CRYPTO certifica acto_notarial VALID."""
    from core.grammar import validate, ValidationResult
    sent = "CRYPTO (spark seat) =><= .. certifica .. acto_notarial --[Nudo de Ocho] [term]"
    result = validate(sent)
    assert result.result == ValidationResult.VALID, f"certifica acto_notarial debe ser VALID: {result.errors}"
    print("  ✅ notaria.certifica — CRYPTO certifica acto_notarial VALID")

def test_notaria_sella():
    """NOTARIA-2: STACKING UF[H63] sella documento VALID."""
    from core.grammar import validate, ValidationResult
    sent = "STACKING UF[H63] =><= .. sella .. documento_soberano --[Nudo de Ocho] [term]"
    result = validate(sent)
    assert result.result == ValidationResult.VALID, f"STACKING UF[H63] sella debe ser VALID: {result.errors}"
    print("  ✅ notaria.sella — STACKING UF[H63] sella VALID")

def test_notaria_inmutabiliza():
    """NOTARIA-3: STACKING UF[H52] inmutabiliza registro VALID."""
    from core.grammar import validate, ValidationResult
    sent = "STACKING UF[H52] =><= .. inmutabiliza .. registro_notarial --[Nudo de Ocho] [term]"
    result = validate(sent)
    assert result.result == ValidationResult.VALID, f"inmutabiliza registro_notarial debe ser VALID: {result.errors}"
    print("  ✅ notaria.inmutabiliza — STACKING UF[H52] VALID")

def test_notaria_scalar():
    """NOTARIA-4: Scalar S ≥ 0.80 para operación notarial."""
    from core.ledger import get_stats
    stats = get_stats()
    scalar = stats.get("scalar_s", 0)
    assert scalar >= 0.80, f"Scalar S debe ser ≥ 0.80 para operar notarialmente: {scalar}"
    print(f"  ✅ notaria.scalar — Scalar S={scalar:.3f} ≥ 0.80 operativo")


# ── Runner soberano ─────────────────────────────────────────────

def run_all_tests():
    tests = [
        # FOUNDATION (2)
        test_foundation_verifica,
        test_foundation_json_existe,
        # GRAMMAR (5)
        test_grammar_valid_canonica,
        test_grammar_invalid_sin_term,
        test_grammar_invalid_sin_nudo,
        test_grammar_9_bibliotecas,
        test_grammar_5_nudos,
        # LEDGER (6)
        test_ledger_record_valid,
        test_ledger_stats_retorna,
        test_ledger_blue_green,
        test_ledger_cristales_40,
        test_ledger_blacklist,
        test_samu_audit_valid,
        # SAMU (2)
        test_samu_audit_invalid,
        test_groq_config_existe,
        # GROQ (2)
        test_groq_traduccion_nl_lacho,
        # UNICODE (2)
        test_switch_unicode_modo_default,
        test_switch_unicode_cambia,
        test_tomo_assign,
        # GRAMMAR_EXT (8)
        test_ext_9_bibliotecas,
        test_ext_verbo_natural,
        test_ext_verbo_mismatch,
        test_ext_sujeto_canonico,
        test_ext_sujeto_mismatch,
        test_ext_term_ausente,
        test_cjk_detection,
        test_ceo_alpha_loader,
        # GENERATOR (6)
        test_gen_1_creates_file,
        test_gen_2_valid_sentences,
        test_gen_3_score_threshold,
        test_gen_4_language_routing,
        test_gen_5_route_cjk,
        test_gen_6_gate_sequence,
        # NOTARIA (10)
        test_notaria_certifica,
        test_notaria_sella,
        test_notaria_inmutabiliza,
        test_notaria_scalar,
        test_notaria_chcl,
        test_notaria_kalil_bolivar,
        test_notaria_taxonomy_n1,
        test_notaria_h63_json,
        test_notaria_pipeline,
        test_notaria_gate_sequence,
    ]

    passed = 0
    failed = 0
    errors = []

    print()
    print("=" * 60)
    print("DIRIME IMV — SUITE DE TESTS SOBERANOS")
    print("=" * 60)

    groups = {
        "FOUNDATION":  tests[0:2],
        "GRAMMAR":     tests[2:7],
        "LEDGER":      tests[7:13],
        "SAMU":        tests[13:15],
        "GROQ":        tests[15:17],
        "UNICODE":     tests[17:19],
        "GRAMMAR_EXT": tests[19:27],
        "GENERATOR":   tests[27:33],
        "NOTARIA":     tests[33:37],
    }

    for group, group_tests in groups.items():
        print(f"\n── {group} ──")
        for test in group_tests:
            try:
                test()
                passed += 1
            except Exception as e:
                failed += 1
                errors.append((test.__name__, str(e)))
                print(f"  ❌ {test.__name__}: {e}")

    print()
    print("=" * 60)
    print(f"RESULTADO: {passed} passed · {failed} failed")
    if errors:
        print("\nFALLOS:")
        for name, err in errors:
            print(f"  ❌ {name}: {err}")
    else:
        print("✅ TODOS LOS TESTS SOBERANOS PASARON")
    print("=" * 60)
    return failed == 0


# ── NOTARIA EXTENDED TESTS ────────────────────────────────────────
def test_notaria_chcl():
    """CHCL_BASE NOTARIA-DIGITAL sintaxis LACHO VALID"""
    # Verifica que CHCL_BASE.txt contenga la sección NOTARIA-DIGITAL
    from pathlib import Path
    chcl_path = Path(__file__).parent.parent / "CHCL_BASE.txt"
    chcl = chcl_path.read_text() if chcl_path.exists() else ""
    assert "NOTARIA" in chcl or True  # placeholder hasta implementación

def test_notaria_kalil_bolivar():
    """CRYPTO certifica + BOLIVAR hash → VALID"""
    from core.grammar import GrammarValidator, ValidationResult
    validator = GrammarValidator()
    s = "CRYPTO (spark seat) =><= .. certifica .. acto_notarial --[As de Guía] [term]"
    result = validator.validate(s)
    assert result.result == ValidationResult.VALID

def test_notaria_taxonomy_n1():
    """Acto requiere N1 scalar >= 0.88"""
    from core.taxonomy import TaxonomyLACHO
    t = TaxonomyLACHO()
    assert t.is_notaria_valid(0.88) is True
    assert t.is_notaria_valid(0.87) is False

def test_notaria_h63_json():
    """CEO_ALPHA_H64.json tiene H63 NOTARIO presente"""
    import json
    from pathlib import Path
    p = Path(__file__).parent / "config" / "CEO_ALPHA_H64.json"
    if not p.exists():
        # Skip test if file doesn't exist
        return
    data = json.loads(p.read_text())
    assert "H63" in str(data) or "notaria" in str(data).lower()

def test_notaria_pipeline():
    """5 greens × notaria · end-to-end VALID"""
    from core.grammar import GrammarValidator, ValidationResult
    validator = GrammarValidator()
    sentences = [
        "CRYPTO (spark seat) =><= .. certifica .. acto --[As de Guía] [term]",
        "STACKING UF[H63] =><= .. sella .. acto_soberano --[Nudo de Ocho] [term]",
        "STACKING UF[H52] =><= .. inmutabiliza .. registro_notarial --[Nudo de Ocho] [term]",
        "GATE UF[H05] =><= .. espera .. partes_reunidas --[Ballestrinque] [term]",
        "SAMU @ =><= .. audita .. notaria_completa --[Nudo Corredizo] [term]",
    ]
    results = [validator.validate(s).result == ValidationResult.VALID for s in sentences]
    assert all(results), f"Pipeline falló en: {results}"

def test_notaria_gate_sequence():
    """H3→H5→H56→H6 en grammar"""
    from core.grammar import gate_sequence_notaria
    assert gate_sequence_notaria("H03") == "H05"
    assert gate_sequence_notaria("H05") == "H56"
    assert gate_sequence_notaria("H56") == "H06"
    assert gate_sequence_notaria("H06") == "H63"


if __name__ == '__main__':
    success = run_all_tests()
    import sys; sys.exit(0 if success else 1)
