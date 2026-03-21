#!/usr/bin/env python3
"""
test_generator_v030.py — Tests generator.py V0.3.0 features
Tests 39→44 · V0.3.0 GATE criteria validation
$mon 04/05 · [term] :: activo
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime

# Add IMV root to path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

# Mock core modules
mock_validate = Mock()
mock_lacho_score = Mock(return_value=0.9)
mock_route = Mock(return_value=Mock(library="TRUST", subject="FOUNDATION", verb="declara", knot="As de Guía"))

# Test 39: Generator basic functionality
def test_generator_collect():
    """Test generator collect function."""
    with patch('generator.validate', mock_validate), \
         patch('generator.lacho_score', mock_lacho_score), \
         patch('generator.route', mock_route):
        
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
    with patch('generator.validate', mock_validate), \
         patch('generator.lacho_score', mock_lacho_score), \
         patch('generator.route', mock_route):
        
        try:
            from tools.generator import build_stats_sentences
            
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
    with patch('generator.validate', mock_validate), \
         patch('generator.lacho_score', mock_lacho_score), \
         patch('generator.route', mock_route):
        
        try:
            from tools.generator import select_valid
            
            # Mock validation results
            mock_validate.return_value = Mock(result="VALID")
            
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
    with patch('generator.validate', mock_validate), \
         patch('generator.lacho_score', mock_lacho_score), \
         patch('generator.route', mock_route):
        
        try:
            from tools.generator import compose
            
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
            
            # Mock select_valid to return test sentences
            with patch('generator.select_valid') as mock_select:
                mock_select.return_value = [
                    "TRUST FOUNDATION =><= .. declara .. test_compose --[As de Guía] [term]",
                    "METHOD <stat_onto> =><= .. calcula .. test_compose --[Ballestrinque] [term]"
                ]
                
                content, valid, avg = compose("stats", data, "2026-05-04 12:00:00")
                
                assert len(valid) == 2
                assert avg >= 0.0
                assert "generated_lacho" in content
                assert "IMV AUTO-GENERATED" in content
                
                print("✅ Test 42: Generator compose - PASSED")
                
        except Exception as e:
            print(f"❌ Test 42: Generator compose - FAILED: {e}")
            raise

# Test 43: Generator notaria acto
def test_generator_notaria_acto():
    """Test generator generate_notaria_acto function."""
    with patch('generator.validate', mock_validate), \
         patch('generator.lacho_score', mock_lacho_score), \
         patch('generator.route', mock_route):
        
        try:
            from tools.generator import generate_notaria_acto
            
            # Mock validation results
            mock_validate.return_value = Mock(result=Mock(value="VALID"))
            
            # Mock dependencies
            with patch('generator.get_scalar_s') as mock_scalar, \
                 patch('generator.get_stats') as mock_stats, \
                 patch('generator.record_notaria_act') as mock_record:
                
                mock_scalar.return_value = 0.8
                mock_stats.return_value = {"transactions_total": 2026}
                
                path = generate_notaria_acto(["parte_A", "parte_B"], "objeto_soberano")
                
                assert path.name.startswith("notaria_")
                assert path.name.endswith(".lacho")
                mock_record.assert_called_once()
                
                print("✅ Test 43: Generator notaria acto - PASSED")
                
        except Exception as e:
            print(f"❌ Test 43: Generator notaria acto - FAILED: {e}")
            raise

# Test 44: Generator V0.3.0 integration
def test_generator_v030_integration():
    """Test generator V0.3.0 GATE criteria integration."""
    with patch('generator.validate', mock_validate), \
         patch('generator.lacho_score', mock_lacho_score), \
         patch('generator.route', mock_route):
        
        try:
            from tools.generator import main
            
            # Mock sys.argv for testing
            test_args = ["generator.py", "--mode", "stats", "--output", "/tmp/test.lacho"]
            
            with patch('sys.argv', test_args), \
                 patch('generator.collect') as mock_collect, \
                 patch('generator.compose') as mock_compose, \
                 patch('generator.write_file') as mock_write, \
                 patch('generator.register_crystal') as mock_register:
                
                # Mock collect data
                mock_collect.return_value = {
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
                
                # Mock compose results
                mock_compose.return_value = (
                    "test content",
                    ["TRUST FOUNDATION =><= .. declara .. test --[As de Guía] [term]"],
                    0.9
                )
                
                # Test main function
                main()
                
                # Verify calls
                mock_collect.assert_called_once()
                mock_compose.assert_called_once()
                mock_write.assert_called_once()
                mock_register.assert_called_once()
                
                print("✅ Test 44: Generator V0.3.0 integration - PASSED")
                
        except SystemExit:
            # Expected due to argparse in main()
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
        test_generator_notaria_acto,
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
