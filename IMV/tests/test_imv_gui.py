#!/usr/bin/env python3
"""
DIRIME IMV — tests/test_imv_gui.py
Tests GUI Tkinter soberana · Tests 33→38
V1 · $thu 30/04 · [term] :: activo
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add IMV root to path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# Mock tkinter since it's not available in test environment
sys.modules['tkinter'] = Mock()
sys.modules['tkinter.ttk'] = Mock()
sys.modules['tkinter.scrolledtext'] = Mock()

# Mock core modules
mock_validate = Mock()
mock_lacho_score = Mock(return_value=0.9)
mock_route = Mock(return_value="test_route")
mock_get_stats = Mock(return_value={
    "transactions_total": 2026,
    "scalar_s": 0.8,
    "crystals_total": 60
})

# Test 33: GUI initialization
def test_gui_initialization():
    """Test GUI basic initialization."""
    with patch('interface.gui.validate', mock_validate), \
         patch('interface.gui.lacho_score', mock_lacho_score), \
         patch('interface.gui.route', mock_route), \
         patch('interface.gui.get_stats', mock_get_stats):
        
        try:
            from interface.gui import IMVGui
            
            # Mock root
            mock_root = Mock()
            mock_root.title = Mock()
            mock_root.configure = Mock()
            mock_root.minsize = Mock()
            
            # Create GUI instance
            gui = IMVGui(mock_root)
            
            # Verify basic attributes
            assert hasattr(gui, 'root')
            assert hasattr(gui, 'lib_var')
            assert hasattr(gui, 'subj_var')
            assert hasattr(gui, 'verb_var')
            assert hasattr(gui, 'obj_var')
            assert hasattr(gui, 'knot_var')
            
            print("✅ Test 33: GUI initialization - PASSED")
            
        except Exception as e:
            print(f"❌ Test 33: GUI initialization - FAILED: {e}")
            raise

# Test 34: Sentence building
def test_sentence_building():
    """Test LACHO sentence building functionality."""
    with patch('interface.gui.validate', mock_validate), \
         patch('interface.gui.lacho_score', mock_lacho_score), \
         patch('interface.gui.route', mock_route), \
         patch('interface.gui.get_stats', mock_get_stats):
        
        try:
            from interface.gui import IMVGui
            
            # Mock root and widgets
            mock_root = Mock()
            mock_root.title = Mock()
            mock_root.configure = Mock()
            mock_root.minsize = Mock()
            
            gui = IMVGui(mock_root)
            
            # Mock GUI components
            gui.lib_var = Mock(get=lambda: "SOCIAL")
            gui.subj_var = Mock(get=lambda: "{relay}")
            gui.verb_var = Mock(get=lambda: "transmite")
            gui.obj_var = Mock(get=lambda: "relay_kalil_soberano")
            gui.knot_var = Mock(get=lambda: "As de Guía")
            gui.sentence_label = Mock(config=Mock())
            gui.log_text = Mock(insert=Mock(), see=Mock())
            
            # Test sentence building
            gui._build_sentence()
            
            # Verify sentence label was updated
            gui.sentence_label.config.assert_called_once()
            
            print("✅ Test 34: Sentence building - PASSED")
            
        except Exception as e:
            print(f"❌ Test 34: Sentence building - FAILED: {e}")
            raise

# Test 35: Validation functionality
def test_validation_functionality():
    """Test sentence validation functionality."""
    with patch('interface.gui.validate', mock_validate), \
         patch('interface.gui.lacho_score', mock_lacho_score), \
         patch('interface.gui.route', mock_route), \
         patch('interface.gui.get_stats', mock_get_stats):
        
        try:
            from interface.gui import IMVGui
            
            # Mock root and widgets
            mock_root = Mock()
            mock_root.title = Mock()
            mock_root.configure = Mock()
            mock_root.minsize = Mock()
            
            gui = IMVGui(mock_root)
            
            # Mock validation result
            mock_result = Mock()
            mock_result.value = "VALID"
            mock_result.errors = []
            mock_result.warnings = []
            mock_validate.return_value = mock_result
            
            # Mock GUI components
            gui.sentence_label = Mock(cget=lambda x: "SOCIAL {relay} =><= .. transmite .. relay_kalil_soberano --[As de Guía] [term]")
            gui.val_result = Mock(config=Mock())
            gui.score_label = Mock(config=Mock())
            gui.log_text = Mock(insert=Mock(), see=Mock())
            
            # Test validation
            gui._validate_sentence()
            
            # Verify validation was called
            mock_validate.assert_called_once()
            mock_lacho_score.assert_called_once()
            
            print("✅ Test 35: Validation functionality - PASSED")
            
        except Exception as e:
            print(f"❌ Test 35: Validation functionality - FAILED: {e}")
            raise

# Test 36: Routing functionality
def test_routing_functionality():
    """Test sentence routing functionality."""
    with patch('interface.gui.validate', mock_validate), \
         patch('interface.gui.lacho_score', mock_lacho_score), \
         patch('interface.gui.route', mock_route), \
         patch('interface.gui.get_stats', mock_get_stats):
        
        try:
            from interface.gui import IMVGui
            
            # Mock root and widgets
            mock_root = Mock()
            mock_root.title = Mock()
            mock_root.configure = Mock()
            mock_root.minsize = Mock()
            
            gui = IMVGui(mock_root)
            
            # Mock GUI components
            gui.sentence_label = Mock(cget=lambda x: "SOCIAL {relay} =><= .. transmite .. relay_kalil_soberano --[As de Guía] [term]")
            gui.log_text = Mock(insert=Mock(), see=Mock())
            
            # Test routing
            gui._route_sentence()
            
            # Verify route was called
            mock_route.assert_called_once()
            
            print("✅ Test 36: Routing functionality - PASSED")
            
        except Exception as e:
            print(f"❌ Test 36: Routing functionality - FAILED: {e}")
            raise

# Test 37: Clear builder functionality
def test_clear_builder_functionality():
    """Test clear builder functionality."""
    with patch('interface.gui.validate', mock_validate), \
         patch('interface.gui.lacho_score', mock_lacho_score), \
         patch('interface.gui.route', mock_route), \
         patch('interface.gui.get_stats', mock_get_stats):
        
        try:
            from interface.gui import IMVGui
            
            # Mock root and widgets
            mock_root = Mock()
            mock_root.title = Mock()
            mock_root.configure = Mock()
            mock_root.minsize = Mock()
            
            gui = IMVGui(mock_root)
            
            # Mock GUI components
            gui.subj_var = Mock(set=Mock())
            gui.obj_var = Mock(set=Mock())
            gui.sentence_label = Mock(config=Mock())
            gui.val_result = Mock(config=Mock())
            gui.score_label = Mock(config=Mock())
            gui.log_text = Mock(insert=Mock(), see=Mock())
            
            # Test clear builder
            gui._clear_builder()
            
            # Verify clear operations
            gui.subj_var.set.assert_called_once_with("")
            gui.obj_var.set.assert_called_once_with("")
            
            print("✅ Test 37: Clear builder functionality - PASSED")
            
        except Exception as e:
            print(f"❌ Test 37: Clear builder functionality - FAILED: {e}")
            raise

# Test 38: Stats update functionality
def test_stats_update_functionality():
    """Test stats update functionality."""
    with patch('interface.gui.validate', mock_validate), \
         patch('interface.gui.lacho_score', mock_lacho_score), \
         patch('interface.gui.route', mock_route), \
         patch('interface.gui.get_stats', mock_get_stats):
        
        try:
            from interface.gui import IMVGui
            
            # Mock root and widgets
            mock_root = Mock()
            mock_root.title = Mock()
            mock_root.configure = Mock()
            mock_root.minsize = Mock()
            
            gui = IMVGui(mock_root)
            
            # Mock GUI components
            gui.stats_label = Mock(config=Mock())
            
            # Reset mock call count
            mock_get_stats.reset_mock()
            
            # Test stats update
            gui._update_stats()
            
            # Verify stats were retrieved and label updated
            mock_get_stats.assert_called_once()
            gui.stats_label.config.assert_called_once()
            
            print("✅ Test 38: Stats update functionality - PASSED")
            
        except Exception as e:
            print(f"❌ Test 38: Stats update functionality - FAILED: {e}")
            raise


if __name__ == "__main__":
    print("🧪 Running GUI Tests (33-38)")
    print("=" * 50)
    
    test_functions = [
        test_gui_initialization,
        test_sentence_building,
        test_validation_functionality,
        test_routing_functionality,
        test_clear_builder_functionality,
        test_stats_update_functionality
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
        print("🎉 All GUI tests passed!")
    else:
        print("⚠️ Some tests failed")
        sys.exit(1)
