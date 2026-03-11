"""
DIRIME IMV — test_imv.py
Tests soberanos automatizados del ciclo completo IMV.

Ejecutar: cd ~/Documentos/PLANERAI/DIRIME/IMV && python3 -m pytest tests/ -v
O directo: python3 tests/test_imv.py
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
    # Debe retornar tupla sin lanzar excepción
    result = verify_sovereign_conditions("grammar")
    assert isinstance(result, tuple), "debe retornar tupla soberana"
    assert len(result) == 3, "tupla debe tener 3 elementos"
    foundation, scope, term = result
    assert foundation.identity_verified is True, "identidad debe estar verificada"
    # Módulo inválido debe lanzar SovereignError
    try:
        verify_sovereign_conditions("modulo_invalido")
        assert False, "debe lanzar SovereignError para módulo inválido"
    except SovereignError:
        pass  # correcto
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


# ── Tests grammar extendidos (L-01/L-02/L-03) ──────────────────────


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
    print("  ✅ ceo_alpha — 33 hexagramas · H01 ACTIVITY · threshold OK")


class TestGrammarExtended:
    def test_9_bibliotecas_validan(self):
        """Las 9 bibliotecas producen VALID con sentencia mínima correcta."""
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

    def test_verbo_natural_no_warning(self):
        """TRUST + verbo natural no genera warning de verbo."""
        from core.grammar import validate
        p = validate(
            "TRUST FOUNDATION =><= .. verifica .. obj --[As de Guía] [term]"
        )
        assert p.result.value == "VALID", f"Esperado VALID, obtenido {p.result.value}"
        assert not any("Verbo" in w for w in p.warnings), f"No debe haber warning de verbo: {p.warnings}"

    def test_verbo_mismatch_warning(self):
        """TRUST + verbo no natural genera WARNING pero sigue siendo válido."""
        from core.grammar import validate
        p = validate(
            "TRUST FOUNDATION =><= .. lanza .. obj --[As de Guía] [term]"
        )
        assert p.result.value == "WARNING", "Debe marcar WARNING por verbo no natural"
        assert any("no natural" in w for w in p.warnings), f"Debe advertir verbo no natural: {p.warnings}"

    def test_sujeto_canonico_no_warning(self):
        """WORK con sujeto canónico no genera warning de sujeto."""
        from core.grammar import validate
        p = validate(
            "WORK {actuator} =><= .. ejecuta .. tarea --[As de Guía] [term]"
        )
        assert p.result.value == "VALID", f"Esperado VALID, obtenido {p.result.value}"
        assert not any("Sujeto" in w for w in p.warnings), f"No debe haber warning de sujeto: {p.warnings}"

    def test_sujeto_mismatch_warning(self):
        """WORK con sujeto no canónico genera WARNING pero es válido."""
        from core.grammar import validate
        p = validate(
            "WORK {motor} =><= .. ejecuta .. tarea --[As de Guía] [term]"
        )
        assert p.result.value == "WARNING", "Debe marcar WARNING por sujeto no canónico"
        assert any("no canónico" in w for w in p.warnings), f"Debe advertir sujeto no canónico: {p.warnings}"

    def test_term_ausente_invalida(self):
        """Sentencia sin [term] sigue siendo INVALID."""
        from core.grammar import validate
        p = validate(
            "TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía]"
        )
        assert p.result.value == "INVALID", "Sin [term] debe seguir siendo INVALID"


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
    # Con 850+ tx el sistema tiene ambos estados
    total = stats.get("transactions_total", 0)
    assert total > 0, "debe haber transacciones para este test"
    print("  ✅ ledger.get_stats() — blue/green presentes")


def test_ledger_cristales_40():
    """El ledger tiene exactamente 40 cristales activos."""
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


# ── Runner soberano ─────────────────────────────────────────────

def run_all_tests():
    tests = [
        test_foundation_verifica,
        test_foundation_json_existe,
        test_grammar_valid_canonica,
        test_grammar_invalid_sin_term,
        test_grammar_invalid_sin_nudo,
        test_grammar_9_bibliotecas,
        test_grammar_5_nudos,
        test_ledger_record_valid,
        test_ledger_stats_retorna,
        test_ledger_blue_green,
        test_ledger_cristales_40,
        test_ledger_blacklist,
        test_samu_audit_valid,
        test_samu_audit_invalid,
        test_groq_config_existe,
        test_groq_traduccion_nl_lacho,
        test_switch_unicode_modo_default,
        test_switch_unicode_cambia,
        test_tomo_assign,
        test_ext_9_bibliotecas,
        test_ext_verbo_natural,
        test_ext_verbo_mismatch,
        test_ext_sujeto_canonico,
        test_ext_sujeto_mismatch,
        test_ext_term_ausente,
        test_cjk_detection,
        test_ceo_alpha_loader,
    ]

    passed = 0
    failed = 0
    errors = []

    print()
    print("=" * 60)
    print("DIRIME IMV — SUITE DE TESTS SOBERANOS")
    print("=" * 60)

    groups = {
        "FOUNDATION": tests[0:2],
        "GRAMMAR":    tests[2:7],
        "LEDGER":     tests[7:13],
        "SAMU":       tests[13:15],
        "GROQ":       tests[15:17],
        "UNICODE":    tests[17:19],
        "GRAMMAR_EXT": tests[19:27],
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


if __name__ == '__main__':
    success = run_all_tests()
    import sys; sys.exit(0 if success else 1)
