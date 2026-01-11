


import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import os

class JSONReporter:
    """Enhanced JSON reporter with test history and statistics"""
    
    def __init__(self, output_dir: str = "./outputs"):
        self.output_dir = Path(output_dir)
        self.reports_dir = self.output_dir / "reports"
        self.history_file = self.output_dir / "test_history.json"
        
        # Ensure directories exist
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing history
        self.history = self._load_history()
    
    def save_enhanced_report(self, test_result: Dict[str, Any]) -> str:
        """
        Save enhanced JSON report with additional statistics
        
        Args:
            test_result: Test result dictionary from test_executor
            
        Returns:
            Path to saved JSON report
        """
        # Add statistics
        enhanced_result = self._add_statistics(test_result)
        
        # Save to file
        test_id = test_result.get('test_id', datetime.now().strftime("%Y%m%d_%H%M%S"))
        report_filename = f"enhanced_report_{test_id}.json"
        report_path = self.reports_dir / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_result, f, indent=2, default=str)
        
        # Add to history
        self._add_to_history(enhanced_result)
        
        print(f"✓ Enhanced JSON report saved: {report_path}")
        return str(report_path)
    
    def _add_statistics(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Add statistical information to test result"""
        enhanced = test_result.copy()
        
        # Calculate statistics
        stats = {
            "total_steps": len(test_result.get('logs', [])),
            "error_count": len(test_result.get('errors', [])),
            "screenshot_count": len(test_result.get('screenshots', [])),
            "success_rate": 100.0 if test_result.get('success', False) else 0.0,
            "execution_date": datetime.now().strftime("%Y-%m-%d"),
            "execution_time_formatted": f"{test_result.get('execution_time', 0):.2f}s"
        }
        
        enhanced['statistics'] = stats
        
        return enhanced
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load test execution history"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load history: {e}")
                return []
        return []
    
    def _save_history(self):
        """Save test execution history"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save history: {e}")
    
    def _add_to_history(self, test_result: Dict[str, Any]):
        """Add test result to history"""
        # Create summary for history
        summary = {
            "test_id": test_result.get('test_id'),
            "timestamp": test_result.get('timestamp'),
            "success": test_result.get('success'),
            "execution_time": test_result.get('execution_time'),
            "target_url": test_result.get('target_url'),
            "message": test_result.get('message'),
            "error_count": len(test_result.get('errors', [])),
            "screenshot_count": len(test_result.get('screenshots', []))
        }
        
        # Add to history (keep last 100 tests)
        self.history.append(summary)
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        # Save updated history
        self._save_history()
    
    def get_test_statistics(self) -> Dict[str, Any]:
        """
        Get overall test statistics from history
        
        Returns:
            Dictionary with test statistics
        """
        if not self.history:
            return {
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "success_rate": 0.0,
                "average_execution_time": 0.0
            }
        
        total = len(self.history)
        passed = sum(1 for test in self.history if test.get('success', False))
        failed = total - passed
        
        avg_time = sum(test.get('execution_time', 0) for test in self.history) / total
        
        return {
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": failed,
            "success_rate": (passed / total * 100) if total > 0 else 0.0,
            "average_execution_time": avg_time,
            "last_test": self.history[-1] if self.history else None
        }
    
    def get_recent_tests(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent test results
        
        Args:
            count: Number of recent tests to retrieve
            
        Returns:
            List of recent test summaries
        """
        return self.history[-count:] if self.history else []
    
    def get_test_by_id(self, test_id: str) -> Dict[str, Any]:
        """
        Get specific test result by ID
        
        Args:
            test_id: Test ID to search for
            
        Returns:
            Test result dictionary or None
        """
        # Search in history
        for test in self.history:
            if test.get('test_id') == test_id:
                # Try to load full report
                report_path = self.reports_dir / f"enhanced_report_{test_id}.json"
                if report_path.exists():
                    with open(report_path, 'r') as f:
                        return json.load(f)
                return test
        
        return None
    
    def get_success_rate_trend(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get success rate trend over time
        
        Args:
            days: Number of days to analyze
            
        Returns:
            List of daily success rates
        """
        from collections import defaultdict
        
        daily_stats = defaultdict(lambda: {"total": 0, "passed": 0})
        
        # Group tests by date
        for test in self.history:
            timestamp = test.get('timestamp', '')
            if timestamp:
                # Extract date from ISO timestamp
                date = timestamp.split('T')[0]
                daily_stats[date]["total"] += 1
                if test.get('success', False):
                    daily_stats[date]["passed"] += 1
        
        # Calculate success rates
        trend = []
        for date, stats in sorted(daily_stats.items())[-days:]:
            success_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            trend.append({
                "date": date,
                "total_tests": stats["total"],
                "passed_tests": stats["passed"],
                "success_rate": round(success_rate, 2)
            })
        
        return trend
    
    def export_history(self, output_path: str = None) -> str:
        """
        Export test history to JSON file
        
        Args:
            output_path: Optional custom output path
            
        Returns:
            Path to exported file
        """
        if output_path is None:
            output_path = self.output_dir / f"test_history_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "total_tests": len(self.history),
            "statistics": self.get_test_statistics(),
            "history": self.history
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"✓ History exported to: {output_path}")
        return str(output_path)
    
    def clear_old_reports(self, days: int = 30):
        """
        Clear reports older than specified days
        
        Args:
            days: Age threshold in days
        """
        import time
        
        cutoff_time = time.time() - (days * 86400)
        deleted_count = 0
        
        for report_file in self.reports_dir.glob("enhanced_report_*.json"):
            if report_file.stat().st_mtime < cutoff_time:
                report_file.unlink()
                deleted_count += 1
        
        print(f"✓ Deleted {deleted_count} old reports")


# Example usage
if __name__ == "__main__":
    # Test the reporter
    reporter = JSONReporter()
    
    # Sample test result
    sample_result = {
        "test_id": "20250106_151500",
        "success": True,
        "message": "Test completed successfully",
        "execution_time": 4.23,
        "target_url": "https://example.com",
        "timestamp": datetime.now().isoformat(),
        "screenshots": ["screenshot1.png"],
        "errors": [],
        "logs": ["Starting test...", "Test completed"]
    }
    
    # Save enhanced report
    report_path = reporter.save_enhanced_report(sample_result)
    print(f"\n✓ Report saved: {report_path}")
    
    # Get statistics
    stats = reporter.get_test_statistics()
    print(f"\n📊 Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Get recent tests
    recent = reporter.get_recent_tests(5)
    print(f"\n📋 Recent Tests: {len(recent)}")

