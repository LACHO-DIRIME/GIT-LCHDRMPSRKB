#!/usr/bin/env python3
"""
Tests para validación por paradigma - grammar.py
Verificación de TAREA_W04 - _validate_by_paradigm implementación
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.grammar import validate

def test_social_forbidden_verb():
    """Test: SOCIAL prohibe verbos de ejecución directa"""
    p = validate("SOCIAL {chair} =><= .. ignite .. proceso --[As de Guía] [term]")
    print(f"Test SOCIAL forbidden verb:")
    print(f"  Result: {p.result.value}")
    print(f"  Warnings: {p.warnings}")
    assert any("prohibido" in w.lower() for w in p.warnings), f"Esperado WARNING por ignite, got: {p.warnings}"
    print("  ✅ PASS - Verbo prohibido detectado")
    return True

def test_crypto_requires_seat():
    """Test: CRYPTO requiere sujeto (seat)"""
    p = validate("CRYPTO FOUNDATION =><= .. certifica .. objeto --[Nudo de Ocho] [term]")
    print(f"\nTest CRYPTO requires seat:")
    print(f"  Result: {p.result.value}")
    print(f"  Warnings: {p.warnings}")
    assert any("seat" in w.lower() for w in p.warnings), f"Esperado WARNING por seat, got: {p.warnings}"
    print("  ✅ PASS - Requerimiento seat detectado")
    return True

def test_gate_valid_hexagram():
    """Test: GATE valida hexagramas canónicos"""
    p = validate("GATE UF[H05] =><= .. contiene .. partes --[Ballestrinque] [term]")
    print(f"\nTest GATE valid hexagram:")
    print(f"  Result: {p.result.value}")
    print(f"  Warnings: {p.warnings}")
    assert p.result.value in ["VALID","WARNING"], f"Expected VALID or WARNING, got: {p.result.value}"
    print("  ✅ PASS - Hexagrama válido aceptado")
    return True

def test_method_requires_operator():
    """Test: METHOD requiere operador del set canónico"""
    p = validate("METHOD <equation> =><= .. calcula .. ratio --[Ballestrinque] [term]")
    print(f"\nTest METHOD requires operator:")
    print(f"  Result: {p.result.value}")
    print(f"  Warnings: {p.warnings}")
    # Si usa operador válido, no debe haber warning
    if "<equation>" in p.subject:
        assert not any("operador" in w.lower() for w in p.warnings), f"No esperado WARNING con operador válido: {p.warnings}"
    print("  ✅ PASS - Operador METHOD válido")
    return True

def test_social_valid_verb():
    """Test: SOCIAL acepta verbos descriptivos válidos"""
    p = validate("SOCIAL {chair} =><= .. distribuye .. recursos --[As de Guía] [term]")
    print(f"\nTest SOCIAL valid verb:")
    print(f"  Result: {p.result.value}")
    print(f"  Warnings: {p.warnings}")
    # No debe haber warning por verbo prohibido
    assert not any("prohibido" in w.lower() for w in p.warnings), f"No esperado WARNING con verbo válido: {p.warnings}"
    print("  ✅ PASS - Verbo SOCIAL válido aceptado")
    return True

if __name__ == "__main__":
    print("🧪 Testing TAREA_W04 - Paradigm Validation Implementation")
    print("=" * 60)
    
    tests = [
        test_social_forbidden_verb,
        test_crypto_requires_seat,
        test_gate_valid_hexagram,
        test_method_requires_operator,
        test_social_valid_verb,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"  ❌ FAIL")
        except Exception as e:
            failed += 1
            print(f"  ❌ ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! TAREA_W04 implementation successful")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed - review implementation")
        sys.exit(1)
