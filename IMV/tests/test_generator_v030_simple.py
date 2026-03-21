#!/usr/bin/env python3
"""
test_generator_v030_simple.py — Tests generator.py V0.3.0 features (simplified)
Tests 39→44 · V0.3.0 GATE criteria validation
$mon 04/05 · [term] :: activo
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add IMV root to path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

# Test 39: Generator basic functionality
def test_generator_collect():
    """Test generator collect function."""
    try:
        from generator import collect
        
        # Mock get_stats and other functions
        with patch('generator.get_stats') as mock_stats, \
             patch('generator.get_recent') as mock_recent, \
             patch('generator.export_crystals_report') as mock_crystals, \
             patch('generator.get_library_stats') as mock_lib_stats, \
             patch('generator.get_verb_frequency') as mock_verb_freq:
            
            mock_stats.return_value = {
                "transactions_total": 2026,
                "lacho_score": 0.8,
                "crystals_total": 60,
                "grammar_valid": 1121,
                "green_count": 320
            }
            mock_recent.return_value = []
            mock_crystals.return_value = {"crystals": []}
            mock_lib_stats.return_value = []
            mock_verb_freq.return_value = []
            
            data = collect()
            
            assert "stats" in data
            assert "recent" in data
            assert "crystals" in data
            assert "lib_stats" in data
            assert "verb_freq" in data
            
            print("✅ Test 39: Generator collect - PASSED")
            
    except Exception as e:
        print(f"❌ Test 39: Generator collect - FAILED: {e}")
        raise

# Test 40: Generator stats sentences
def test_generator_build_stats_sentences():
    """Test generator build_stats_sentences function."""
    try:
        from generator import build_stats_sentences
        
        data = {
            "stats": {
                "transactions_total": 2026,
                "lacho_score": 0.8,
                "crystals_total": 60,
                "grammar_valid": 1121,
                "green_count": 320
            }
        }
        
        sentences = build_stats_sentences(data)
        
        assert len(sentences) == 5
        assert "TX_2026_soberano" in sentences[0]
        assert "scalar_s_0.8_activo" in sentences[1]
        assert "cristales_60_verificados" in sentences[2]
        assert "grammar_valid_1121_sentencias" in sentences[3]
        assert "green_320_WU_activos" in sentences[4]
        
        print("✅ Test 40: Generator stats sentences - PASSED")
        
    except Exception as e:
        print(f"❌ Test 40: Generator stats sentences - FAILED: {e}")
        raise

# Test 41: Generator select valid sentences
def test_generator_select_valid():
    """Test generator select_valid function."""
    try:
        from generator import select_valid, validate, lacho_score
        
        # Mock validation results
        mock_result = Mock()
        mock_result.result = "VALID"
        
        with patch('generator.validate', return_value=mock_result), \
             patch('generator.lacho_score', return_value=0.9):
            
            sentences = [
                "TRUST FOUNDATION =><= .. declara .. test_valid --[As de Guía] [term]",
                "WORK {actuator} =><= .. ejecuta .. test_invalid --[As de Guía] [term]",
                "METHOD <stat_onto> =><= .. calcula .. test_valid --[Ballestrinque] [term]"
            ]
            
            valid = select_valid(sentences, threshold=0.6)
            
            assert len(valid) == 3  # All should pass with mock
            
            print("✅ Test 41: Generator select valid - PASSED")
            
    except Exception as e:
        print(f"❌ Test 41: Generator select valid - FAILED: {e}")
        raise

# Test 42: Generator compose function
def test_generator_compose():
    """Test generator compose function."""
    try:
        from generator import compose, validate, lacho_score
        
        # Mock validation results
        mock_result = Mock()
        mock_result.result = "VALID"
        
        data = {
            "stats": {
                "transactions_total": 2026,
                "lacho_score": 0.8,
                "crystals_total": 60,
                "grammar_valid": 1121,
                "green_count": 320
            },
            "recent": [],
            "crystals": {"crystals": []},
            "lib_stats": [],
            "verb_freq": []
        }
        
        with patch('generator.validate', return_value=mock_result), \
             patch('generator.lacho_score', return_value=0.9), \
             patch('generator.select_valid', return_value=[
                 "TRUST FOUNDATION =><= .. declara .. test_compose --[As de Guía] [term]",
                 "METHOD <stat_onto> =><= .. calcula .. test_compose --[Ballestrinque] [term]"
             ]):
            
            content, valid, avg = compose("stats", data, "2026-05-04 12:00:00")
            
            assert len(valid) == 2
            assert avg >= 0.0
            assert "generated_lacho" in content
            assert "IMV AUTO-GENERATED" in content
            
            print("✅ Test 42: Generator compose - PASSED")
            
    except Exception as e:
        print(f"❌ Test 42: Generator compose - FAILED: {e}")
        raise

# Test 43: Generator cabecera function
def test_generator_cabecera():
    """Test generator cabecera function."""
    try:
        from generator import cabecera
        
        stats = {
            "transactions_total": 2026,
            "lacho_score": 0.8,
            "crystals_total": 60
        }
        ts = "2026-05-04 12:00:00"
        avg = 0.85
        n = 5
        
        header = cabecera(stats, ts, avg, n)
        
        assert "IMV AUTO-GENERATED" in header
        assert "2026-05-04 12:00:00" in header
        assert "2026" in header
        assert "60" in header
        assert "0.850" in header
        assert "5" in header
        
        print("✅ Test 43: Generator cabecera - PASSED")
        
    except Exception as e:
        print(f"❌ Test 43: Generator cabecera - FAILED: {e}")
        raise

# Test 44: Generator V0.3.0 integration test
def test_generator_v030_integration():
    """Test generator V0.3.0 basic integration."""
    try:
        from generator import build_stats_sentences, select_valid, cabecera
        
        # Test integration of multiple functions
        data = {
            "stats": {
                "transactions_total": 2026,
                "lacho_score": 0.8,
                "crystals_total": 60,
                "grammar_valid": 1121,
                "green_count": 320
            }
        }
        
        # Build stats sentences
        stats_sentences = build_stats_sentences(data)
        assert len(stats_sentences) == 5
        
        # Mock validation for select_valid
        mock_result = Mock()
        mock_result.result = "VALID"
        
        with patch('generator.validate', return_value=mock_result), \
             patch('generator.lacho_score', return_value=0.9):
            
            # Select valid sentences
            valid = select_valid(stats_sentences)
            assert len(valid) == 5
            
            # Generate header
            header = cabecera(data["stats"], "2026-05-04 12:00:00", 0.9, len(valid))
            assert "IMV AUTO-GENERATED" in header
            
            print("✅ Test 44: Generator V0.3.0 integration - PASSED")
            
    except Exception as e:
        print(f"❌ Test 44: Generator V0.3.0 integration - FAILED: {e}")
        raise


if __name__ == "__main__":
    print("🧪 Running Generator V0.3.0 Tests (39-44)")
    print("=" * 50)
    
    test_functions = [
        test_generator_collect,
        test_generator_build_stats_sentences,
        test_generator_select_valid,
        test_generator_compose,
        test_generator_cabecera,
        test_generator_v030_integration
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"FAILED: {e}")
    
    print("=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")
    print(f"📈 Success Rate: {(passed/(passed+failed))*100:.1f}%")
    
    if failed == 0:
        print("🎉 All generator tests passed!")
    else:
        print("⚠️ Some tests failed")
        sys.exit(1)
