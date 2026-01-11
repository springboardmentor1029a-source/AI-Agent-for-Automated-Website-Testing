

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import traceback
import re


class ErrorHandler:
    """Handles errors during test execution with recovery strategies"""
    
    def __init__(self):
        self.error_log = []
        self.recovery_strategies = {}
        self._register_default_strategies()
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle an error with appropriate recovery strategy
        
        Args:
            error: The exception that occurred
            context: Additional context about where/when error occurred
            
        Returns:
            Dictionary with error details and recovery suggestions
        """
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {},
            "severity": self._assess_severity(error),
            "recoverable": self._is_recoverable(error),
            "recovery_suggestions": []
        }
        
        # Get recovery suggestions
        error_info["recovery_suggestions"] = self._get_recovery_suggestions(error)
        
        # Log the error
        self.error_log.append(error_info)
        
        return error_info
    
    def _assess_severity(self, error: Exception) -> str:
        """
        Assess error severity
        
        Returns:
            'critical', 'high', 'medium', or 'low'
        """
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        # Critical errors
        critical_patterns = [
            'memory', 'fatal', 'system', 'crash', 'kernel',
            'segmentation fault', 'core dumped'
        ]
        
        # High severity errors
        high_patterns = [
            'connection', 'network', 'permission denied',
            'access denied', 'authentication failed'
        ]
        
        # Medium severity errors
        medium_patterns = [
            'timeout', 'not found', 'invalid', 'target closed'
        ]
        
        for pattern in critical_patterns:
            if pattern in error_message:
                return 'critical'
        
        for pattern in high_patterns:
            if pattern in error_message:
                return 'high'
        
        for pattern in medium_patterns:
            if pattern in error_message:
                return 'medium'
        
        return 'low'
    
    def _is_recoverable(self, error: Exception) -> bool:
        """
        Determine if error is recoverable
        
        Returns:
            True if error can be recovered from
        """
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        # Non-recoverable errors
        non_recoverable = [
            'syntaxerror', 'nameerror', 'typeerror',
            'importerror', 'attributeerror'
        ]
        
        if error_type.lower() in non_recoverable:
            return False
        
        # Non-recoverable patterns
        non_recoverable_patterns = [
            'permission denied', 'access denied',
            'out of memory', 'disk full'
        ]
        
        for pattern in non_recoverable_patterns:
            if pattern in error_message:
                return False
        
        return True
    
    def _get_recovery_suggestions(self, error: Exception) -> List[str]:
        """
        Get recovery suggestions for the error
        
        Returns:
            List of recovery suggestions
        """
        suggestions = []
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        # Check registered strategies
        for pattern, strategy in self.recovery_strategies.items():
            if pattern.lower() in error_message or pattern.lower() in error_type.lower():
                suggestions.extend(strategy)
        
        # Default suggestions if none found
        if not suggestions:
            if 'timeout' in error_message:
                suggestions = [
                    "Increase timeout duration",
                    "Check network connectivity",
                    "Verify page load speed",
                    "Add explicit waits before action"
                ]
            elif 'not found' in error_message or 'no such element' in error_message:
                suggestions = [
                    "Verify element selector is correct",
                    "Add wait for element to appear",
                    "Check if element is in iframe",
                    "Try alternative selector strategies"
                ]
            elif 'connection' in error_message or 'network' in error_message:
                suggestions = [
                    "Check internet connectivity",
                    "Verify target URL is accessible",
                    "Check firewall/proxy settings",
                    "Retry with exponential backoff"
                ]
            else:
                suggestions = [
                    "Review error details in logs",
                    "Check test configuration",
                    "Retry the operation",
                    "Contact support if error persists"
                ]
        
        return suggestions
    
    def _register_default_strategies(self):
        """Register default recovery strategies"""
        self.register_recovery_strategy(
            "TimeoutError",
            [
                "Increase page timeout",
                "Add explicit wait before action",
                "Check network connectivity"
            ]
        )
        
        self.register_recovery_strategy(
            "ElementNotFound",
            [
                "Use wait_for_selector before interaction",
                "Try alternative selector (ID, class, text)",
                "Check if element is in iframe or shadow DOM"
            ]
        )
        
        self.register_recovery_strategy(
            "NavigationError",
            [
                "Verify URL is correct and accessible",
                "Check for redirects",
                "Increase navigation timeout"
            ]
        )
    
    def register_recovery_strategy(self, error_pattern: str, suggestions: List[str]):
        """
        Register custom recovery strategy
        
        Args:
            error_pattern: Error type or message pattern
            suggestions: List of recovery suggestions
        """
        self.recovery_strategies[error_pattern] = suggestions
    
    def wrap_function(self, func: Callable, context: Dict[str, Any] = None) -> Callable:
        """
        Wrap a function with error handling
        
        Args:
            func: Function to wrap
            context: Additional context
            
        Returns:
            Wrapped function
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_info = self.handle_error(e, context)
                
                # Log error details
                print(f"\n❌ Error occurred: {error_info['error_type']}")
                print(f"   Message: {error_info['error_message']}")
                print(f"   Severity: {error_info['severity'].upper()}")
                print(f"   Recoverable: {error_info['recoverable']}")
                
                if error_info['recovery_suggestions']:
                    print(f"\n💡 Recovery Suggestions:")
                    for i, suggestion in enumerate(error_info['recovery_suggestions'], 1):
                        print(f"   {i}. {suggestion}")
                
                # Re-raise the exception
                raise
        
        return wrapper
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get summary of all errors
        
        Returns:
            Dictionary with error statistics
        """
        if not self.error_log:
            return {
                "total_errors": 0,
                "by_type": {},
                "by_severity": {},
                "recoverable_count": 0,
                "recent_errors": []
            }
        
        # Count by type
        by_type = {}
        for error in self.error_log:
            error_type = error['error_type']
            by_type[error_type] = by_type.get(error_type, 0) + 1
        
        # Count by severity
        by_severity = {}
        for error in self.error_log:
            severity = error['severity']
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        # Count recoverable
        recoverable = sum(1 for error in self.error_log if error['recoverable'])
        
        return {
            "total_errors": len(self.error_log),
            "by_type": by_type,
            "by_severity": by_severity,
            "recoverable_count": recoverable,
            "recent_errors": self.error_log[-5:]  # Last 5 errors
        }
    
    def clear_log(self):
        """Clear error log"""
        self.error_log.clear()
    
    def export_error_log(self, filepath: str):
        """
        Export error log to JSON file
        
        Args:
            filepath: Path to save error log
        """
        import json
        
        with open(filepath, 'w') as f:
            json.dump(self.error_log, f, indent=2, default=str)
        
        print(f"✓ Error log exported to: {filepath}")


class PlaywrightErrorHandler(ErrorHandler):
    """Specialized error handler for Playwright operations"""
    
    def __init__(self):
        super().__init__()
        self._register_playwright_strategies()
    
    def _register_playwright_strategies(self):
        """Register Playwright-specific recovery strategies"""
        
        self.register_recovery_strategy(
            "Target closed",
            [
                "Page was closed unexpectedly",
                "Check for popups or redirects",
                "Verify page stability before action"
            ]
        )
        
        self.register_recovery_strategy(
            "Element is not attached",
            [
                "Element was removed from DOM",
                "Re-query the element before interaction",
                "Check for dynamic content loading"
            ]
        )
        
        self.register_recovery_strategy(
            "Element is not visible",
            [
                "Wait for element to become visible",
                "Scroll element into view",
                "Check CSS display/visibility properties"
            ]
        )
        
        self.register_recovery_strategy(
            "Navigation timeout",
            [
                "Increase navigation timeout value",
                "Check page load performance",
                "Verify no JavaScript errors blocking load"
            ]
        )
    
    def handle_playwright_error(self, error: Exception, page=None, 
                               action: str = None) -> Dict[str, Any]:
        """
        Handle Playwright-specific error
        
        Args:
            error: The exception
            page: Playwright page object
            action: Action being performed
            
        Returns:
            Error information dictionary
        """
        context = {
            "action": action,
            "page_url": page.url if page else None,
            "page_title": page.title() if page else None
        }
        
        return self.handle_error(error, context)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("ERROR HANDLER - TESTING")
    print("=" * 60)
    
    handler = ErrorHandler()
    
    # Test 1: Handle timeout error
    print("\n[Test 1] Handling Timeout Error")
    print("-" * 60)
    
    try:
        raise TimeoutError("Page load timeout exceeded 30000ms")
    except Exception as e:
        error_info = handler.handle_error(e, {"action": "page.goto"})
        print(f"Error Type: {error_info['error_type']}")
        print(f"Severity: {error_info['severity']}")
        print(f"Recoverable: {error_info['recoverable']}")
        print("\nSuggestions:")
        for suggestion in error_info['recovery_suggestions']:
            print(f"  • {suggestion}")
    
    # Test 2: Handle element not found
    print("\n[Test 2] Handling Element Not Found")
    print("-" * 60)
    
    try:
        raise Exception("Element not found: button#submit")
    except Exception as e:
        error_info = handler.handle_error(e, {"selector": "button#submit"})
        print(f"Severity: {error_info['severity']}")
        print("\nSuggestions:")
        for suggestion in error_info['recovery_suggestions']:
            print(f"  • {suggestion}")
    
    # Test 3: Error summary
    print("\n[Test 3] Error Summary")
    print("-" * 60)
    
    summary = handler.get_error_summary()
    print(f"Total Errors: {summary['total_errors']}")
    print(f"By Type: {summary['by_type']}")
    print(f"By Severity: {summary['by_severity']}")
    print(f"Recoverable: {summary['recoverable_count']}")
    
    print("\n" + "=" * 60)
    print("✅ ERROR HANDLER TESTS COMPLETE")
    print("=" * 60)