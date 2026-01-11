

import pytest
import json
import os
from pathlib import Path
from datetime import datetime
from reporters.html_reporter import HTMLReporter
from reporters.json_reporter import JSONReporter


class TestHTMLReporter:
    """Test HTML report generation"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.output_dir = "./test_outputs"
        self.reporter = HTMLReporter(output_dir=self.output_dir)
        
        self.sample_result = {
            "test_id": "test_20260106_120000",
            "success": True,
            "message": "Test completed successfully",
            "execution_time": 3.45,
            "target_url": "https://example.com",
            "timestamp": datetime.now().isoformat(),
            "screenshots": ["screenshot1.png", "screenshot2.png"],
            "errors": [],
            "logs": ["Starting test", "Test completed"]
        }
    
    def teardown_method(self):
        """Cleanup after tests"""
        # Clean up test outputs
        import shutil
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
    
    def test_reporter_initialization(self):
        """Test reporter initializes correctly"""
        assert self.reporter.output_dir.exists()
        assert self.reporter.html_reports_dir.exists()
        assert self.reporter.screenshots_dir.exists()
    
    def test_generate_html_report(self):
        """Test HTML report generation"""
        html_path = self.reporter.generate_from_test_result(self.sample_result)
        
        assert os.path.exists(html_path)
        assert html_path.endswith('.html')
        
        # Check file content
        with open(html_path, 'r') as f:
            content = f.read()
            assert 'test_20260106_120000' in content
            assert 'Test completed successfully' in content
            assert '3.45s' in content
    
    def test_generate_report_with_errors(self):
        """Test report generation with errors"""
        error_result = self.sample_result.copy()
        error_result['success'] = False
        error_result['errors'] = [
            {
                "type": "TimeoutError",
                "message": "Element not found"
            }
        ]
        
        html_path = self.reporter.generate_from_test_result(error_result)
        
        with open(html_path, 'r') as f:
            content = f.read()
            assert 'FAILED' in content
            assert 'TimeoutError' in content
            assert 'Element not found' in content
    
    def test_generate_report_with_screenshots(self):
        """Test report includes screenshots"""
        html_path = self.reporter.generate_from_test_result(self.sample_result)
        
        with open(html_path, 'r') as f:
            content = f.read()
            assert 'screenshot1.png' in content
            assert 'screenshot2.png' in content
            assert 'Screenshots' in content
    
    def test_list_html_reports(self):
        """Test listing generated reports"""
        # Generate multiple reports
        for i in range(3):
            result = self.sample_result.copy()
            result['test_id'] = f"test_{i}"
            self.reporter.generate_from_test_result(result)
        
        reports = self.reporter.list_html_reports()
        
        assert len(reports) == 3
        assert all('filename' in r for r in reports)
        assert all('path' in r for r in reports)
        assert all('created' in r for r in reports)


class TestJSONReporter:
    """Test JSON report generation and statistics"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.output_dir = "./test_outputs"
        self.reporter = JSONReporter(output_dir=self.output_dir)
        
        self.sample_result = {
            "test_id": "test_20260106_120000",
            "success": True,
            "message": "Test completed",
            "execution_time": 2.5,
            "target_url": "https://example.com",
            "timestamp": datetime.now().isoformat(),
            "screenshots": ["screenshot.png"],
            "errors": [],
            "logs": ["Test log"]
        }
    
    def teardown_method(self):
        """Cleanup after tests"""
        import shutil
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
    
    def test_save_enhanced_report(self):
        """Test saving enhanced JSON report"""
        report_path = self.reporter.save_enhanced_report(self.sample_result)
        
        assert os.path.exists(report_path)
        assert report_path.endswith('.json')
        
        # Check content
        with open(report_path, 'r') as f:
            data = json.load(f)
            assert 'statistics' in data
            assert data['statistics']['total_steps'] > 0
    
    def test_statistics_calculation(self):
        """Test statistics are calculated correctly"""
        report_path = self.reporter.save_enhanced_report(self.sample_result)
        
        with open(report_path, 'r') as f:
            data = json.load(f)
            stats = data['statistics']
            
            assert 'total_steps' in stats
            assert 'error_count' in stats
            assert 'screenshot_count' in stats
            assert 'success_rate' in stats
            assert stats['success_rate'] == 100.0
    
    def test_history_tracking(self):
        """Test test history is tracked"""
        # Save multiple reports
        for i in range(5):
            result = self.sample_result.copy()
            result['test_id'] = f"test_{i}"
            result['success'] = i % 2 == 0  # Alternate pass/fail
            self.reporter.save_enhanced_report(result)
        
        # Check history
        assert len(self.reporter.history) == 5
        
        # Check statistics
        stats = self.reporter.get_test_statistics()
        assert stats['total_tests'] == 5
        assert stats['passed_tests'] == 3
        assert stats['failed_tests'] == 2
    
    def test_get_recent_tests(self):
        """Test getting recent tests"""
        # Generate 15 tests
        for i in range(15):
            result = self.sample_result.copy()
            result['test_id'] = f"test_{i}"
            self.reporter.save_enhanced_report(result)
        
        # Get recent 10
        recent = self.reporter.get_recent_tests(10)
        
        assert len(recent) == 10
        assert recent[-1]['test_id'] == 'test_14'  # Most recent
    
    def test_get_test_by_id(self):
        """Test retrieving specific test"""
        report_path = self.reporter.save_enhanced_report(self.sample_result)
        
        retrieved = self.reporter.get_test_by_id('test_20260106_120000')
        
        assert retrieved is not None
        assert retrieved['test_id'] == 'test_20260106_120000'
        assert retrieved['success'] == True
    
    def test_success_rate_trend(self):
        """Test success rate trend calculation"""
        # Generate tests over multiple days
        for i in range(10):
            result = self.sample_result.copy()
            result['test_id'] = f"test_{i}"
            result['success'] = i % 3 != 0  # ~66% success rate
            self.reporter.save_enhanced_report(result)
        
        trend = self.reporter.get_success_rate_trend(days=7)
        
        assert len(trend) > 0
        assert all('date' in t for t in trend)
        assert all('success_rate' in t for t in trend)
    
    def test_export_history(self):
        """Test exporting history to file"""
        # Generate some tests
        for i in range(3):
            result = self.sample_result.copy()
            result['test_id'] = f"test_{i}"
            self.reporter.save_enhanced_report(result)
        
        # Export
        export_path = self.reporter.export_history()
        
        assert os.path.exists(export_path)
        
        # Verify export content
        with open(export_path, 'r') as f:
            export_data = json.load(f)
            assert 'exported_at' in export_data
            assert 'total_tests' in export_data
            assert 'history' in export_data
            assert len(export_data['history']) == 3
    
    def test_clear_old_reports(self):
        """Test clearing old reports"""
        # Generate reports
        for i in range(5):
            result = self.sample_result.copy()
            result['test_id'] = f"test_{i}"
            self.reporter.save_enhanced_report(result)
        
        # Clear reports older than 0 days (all of them)
        self.reporter.clear_old_reports(days=0)
        
        # Should have no reports left in directory
        report_files = list(self.reporter.reports_dir.glob("enhanced_report_*.json"))
        assert len(report_files) == 0


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
