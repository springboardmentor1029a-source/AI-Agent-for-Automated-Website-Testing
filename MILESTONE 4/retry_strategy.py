

import time
from typing import Callable, Any, Dict, List
from datetime import datetime
import traceback


class RetryStrategy:
    """Handles automatic retries for failed test operations"""
    
    def __init__(self, max_retries: int = 3, initial_delay: float = 1.0, backoff_factor: float = 2.0):
        """
        Initialize retry strategy
        
        Args:
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay between retries (seconds)
            backoff_factor: Multiplier for exponential backoff
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.retry_history = []
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute function with automatic retry on failure
        
        Args:
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Dictionary with execution result and retry information
        """
        result = {
            "success": False,
            "result": None,
            "attempts": 0,
            "errors": [],
            "retry_delays": [],
            "total_time": 0
        }
        
        start_time = time.time()
        delay = self.initial_delay
        
        for attempt in range(1, self.max_retries + 1):
            result["attempts"] = attempt
            
            try:
                print(f"🔄 Attempt {attempt}/{self.max_retries}...")
                
                # Execute the function
                func_result = func(*args, **kwargs)
                
                # Success!
                result["success"] = True
                result["result"] = func_result
                result["total_time"] = time.time() - start_time
                
                print(f"✅ Success on attempt {attempt}")
                
                # Log successful retry
                self._log_retry(attempt, True, None, delay)
                
                return result
                
            except Exception as e:
                error_info = {
                    "attempt": attempt,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "traceback": traceback.format_exc(),
                    "timestamp": datetime.now().isoformat()
                }
                result["errors"].append(error_info)
                
                print(f"❌ Attempt {attempt} failed: {type(e).__name__}: {str(e)}")
                
                # Log failed retry
                self._log_retry(attempt, False, str(e), delay)
                
                # If this wasn't the last attempt, wait before retrying
                if attempt < self.max_retries:
                    result["retry_delays"].append(delay)
                    print(f"⏳ Waiting {delay:.1f}s before retry...")
                    time.sleep(delay)
                    
                    # Exponential backoff
                    delay *= self.backoff_factor
                else:
                    print(f"❌ All {self.max_retries} attempts failed")
        
        result["total_time"] = time.time() - start_time
        return result
    
    def execute_with_conditional_retry(self, func: Callable, should_retry_func: Callable, 
                                      *args, **kwargs) -> Dict[str, Any]:
        """
        Execute function with conditional retry based on error type
        
        Args:
            func: Function to execute
            should_retry_func: Function that takes exception and returns bool (should retry?)
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Dictionary with execution result
        """
        result = {
            "success": False,
            "result": None,
            "attempts": 0,
            "errors": [],
            "retry_delays": [],
            "skipped_retries": 0
        }
        
        delay = self.initial_delay
        
        for attempt in range(1, self.max_retries + 1):
            result["attempts"] = attempt
            
            try:
                func_result = func(*args, **kwargs)
                result["success"] = True
                result["result"] = func_result
                return result
                
            except Exception as e:
                error_info = {
                    "attempt": attempt,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
                result["errors"].append(error_info)
                
                # Check if we should retry for this error type
                if not should_retry_func(e):
                    print(f"⚠️ Error type {type(e).__name__} is not retryable. Stopping.")
                    result["skipped_retries"] = self.max_retries - attempt
                    break
                
                if attempt < self.max_retries:
                    result["retry_delays"].append(delay)
                    time.sleep(delay)
                    delay *= self.backoff_factor
        
        return result
    
    def retry_async_operation(self, func: Callable, timeout: float = 30.0, 
                             *args, **kwargs) -> Dict[str, Any]:
        """
        Retry operation with timeout
        
        Args:
            func: Function to execute
            timeout: Maximum time to wait for operation (seconds)
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Dictionary with execution result
        """
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Operation timed out after {timeout}s")
        
        result = {
            "success": False,
            "result": None,
            "attempts": 0,
            "errors": [],
            "timeouts": 0
        }
        
        for attempt in range(1, self.max_retries + 1):
            result["attempts"] = attempt
            
            try:
                # Set timeout (Unix only)
                if hasattr(signal, 'SIGALRM'):
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(int(timeout))
                
                # Execute function
                func_result = func(*args, **kwargs)
                
                # Cancel timeout
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
                
                result["success"] = True
                result["result"] = func_result
                return result
                
            except TimeoutError as e:
                result["timeouts"] += 1
                result["errors"].append({
                    "attempt": attempt,
                    "error": "TimeoutError",
                    "message": str(e)
                })
                print(f"⏰ Attempt {attempt} timed out")
                
            except Exception as e:
                result["errors"].append({
                    "attempt": attempt,
                    "error": type(e).__name__,
                    "message": str(e)
                })
                print(f"❌ Attempt {attempt} failed: {str(e)}")
            
            finally:
                # Always cancel timeout
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
            
            if attempt < self.max_retries:
                delay = self.initial_delay * (self.backoff_factor ** (attempt - 1))
                time.sleep(delay)
        
        return result
    
    def _log_retry(self, attempt: int, success: bool, error: str, delay: float):
        """Log retry attempt"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "attempt": attempt,
            "success": success,
            "error": error,
            "delay": delay
        }
        self.retry_history.append(log_entry)
    
    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get statistics about retry operations"""
        if not self.retry_history:
            return {
                "total_retries": 0,
                "successful_retries": 0,
                "failed_retries": 0,
                "success_rate": 0.0
            }
        
        total = len(self.retry_history)
        successful = sum(1 for entry in self.retry_history if entry["success"])
        
        return {
            "total_retries": total,
            "successful_retries": successful,
            "failed_retries": total - successful,
            "success_rate": (successful / total * 100) if total > 0 else 0.0,
            "history": self.retry_history[-10:]  # Last 10 retries
        }
    
    def clear_history(self):
        """Clear retry history"""
        self.retry_history.clear()


class PlaywrightRetryStrategy(RetryStrategy):
    """Specialized retry strategy for Playwright operations"""
    
    def __init__(self, max_retries: int = 3):
        super().__init__(max_retries=max_retries, initial_delay=2.0, backoff_factor=1.5)
    
    def should_retry_playwright_error(self, error: Exception) -> bool:
        """
        Determine if Playwright error should be retried
        
        Args:
            error: Exception that occurred
            
        Returns:
            True if error is retryable
        """
        retryable_errors = [
            "TimeoutError",
            "NetworkError", 
            "TargetClosedError",
            "Connection closed",
            "Navigation timeout",
            "Timeout exceeded"
        ]
        
        error_str = str(error)
        error_type = type(error).__name__
        
        # Check if error is retryable
        for retryable in retryable_errors:
            if retryable.lower() in error_str.lower() or retryable.lower() in error_type.lower():
                return True
        
        return False
    
    def execute_playwright_action(self, page, action: str, selector: str = None, 
                                  **action_kwargs) -> Dict[str, Any]:
        """
        Execute Playwright action with retry
        
        Args:
            page: Playwright page object
            action: Action name (click, fill, goto, etc.)
            selector: Element selector (if applicable)
            **action_kwargs: Additional arguments for the action
            
        Returns:
            Execution result dictionary
        """
        def perform_action():
            if action == "goto":
                return page.goto(selector, **action_kwargs)
            elif action == "click":
                return page.click(selector, **action_kwargs)
            elif action == "fill":
                return page.fill(selector, action_kwargs.get('value', ''))
            elif action == "wait_for_selector":
                return page.wait_for_selector(selector, **action_kwargs)
            elif action == "wait_for_load_state":
                return page.wait_for_load_state(selector or "networkidle", **action_kwargs)
            else:
                raise ValueError(f"Unknown action: {action}")
        
        return self.execute_with_conditional_retry(
            perform_action,
            self.should_retry_playwright_error
        )


# Example usage and tests
if __name__ == "__main__":
    print("=" * 60)
    print("RETRY STRATEGY - TESTING")
    print("=" * 60)
    
    # Test 1: Basic retry with eventual success
    print("\n[Test 1] Basic Retry - Simulated Failure then Success")
    print("-" * 60)
    
    attempt_count = {"count": 0}
    
    def flaky_function():
        attempt_count["count"] += 1
        if attempt_count["count"] < 3:
            raise Exception(f"Simulated failure #{attempt_count['count']}")
        return "Success!"
    
    retry = RetryStrategy(max_retries=3, initial_delay=0.5)
    result = retry.execute_with_retry(flaky_function)
    
    print(f"\n✅ Result: {result['success']}")
    print(f"📊 Attempts: {result['attempts']}")
    print(f"⏱️ Total time: {result['total_time']:.2f}s")
    
    # Test 2: All retries fail
    print("\n[Test 2] All Retries Fail")
    print("-" * 60)
    
    def always_fails():
        raise ValueError("This always fails!")
    
    retry2 = RetryStrategy(max_retries=3, initial_delay=0.3)
    result2 = retry2.execute_with_retry(always_fails)
    
    print(f"\n❌ Result: {result2['success']}")
    print(f"📊 Attempts: {result2['attempts']}")
    print(f"🔴 Errors: {len(result2['errors'])}")
    
    # Test 3: Statistics
    print("\n[Test 3] Retry Statistics")
    print("-" * 60)
    stats = retry.get_retry_statistics()
    print(f"Total retries: {stats['total_retries']}")
    print(f"Success rate: {stats['success_rate']:.1f}%")
    
    print("\n" + "=" * 60)
    print("✅ RETRY STRATEGY TESTS COMPLETE")
    print("=" * 60)
