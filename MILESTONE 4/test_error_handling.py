
import pytest
from unittest.mock import Mock, patch
from executors.retry_strategy import RetryStrategy, PlaywrightRetryStrategy
from executors.error_handler import ErrorHandler, PlaywrightErrorHandler
from executors.dom_mapper import DOMMapper


class TestRetryStrategy:
    """Test retry strategy functionality"""
    
    def test_successful_execution_first_try(self):
        """Test function succeeds on first attempt"""
        retry = RetryStrategy(max_retries=3)
        
        def success_func():
            return "Success!"
        
        result = retry.execute_with_retry(success_func)
        
        assert result['success'] == True
        assert result['attempts'] == 1
        assert result['result'] == "Success!"
    
    def test_retry_after_failures(self):
        """Test retry after initial failures"""
        retry = RetryStrategy(max_retries=3, initial_delay=0.1)
        
        attempt_count = {'count': 0}
        
        def flaky_func():
            attempt_count['count'] += 1
            if attempt_count['count'] < 3:
                raise Exception("Temporary failure")
            return "Success on attempt 3"
        
        result = retry.execute_with_retry(flaky_func)
        
        assert result['success'] == True
        assert result['attempts'] == 3
        assert result['result'] == "Success on attempt 3"
    
    def test_max_retries_exceeded(self):
        """Test all retries exhausted"""
        retry = RetryStrategy(max_retries=3, initial_delay=0.1)
        
        def always_fails():
            raise ValueError("Always fails")
        
        result = retry.execute_with_retry(always_fails)
        
        assert result['success'] == False
        assert result['attempts'] == 3
        assert len(result['errors']) == 3
    
    def test_exponential_backoff(self):
        """Test exponential backoff delays"""
        retry = RetryStrategy(max_retries=3, initial_delay=0.5, backoff_factor=2.0)
        
        def always_fails():
            raise Exception("Fail")
        
        result = retry.execute_with_retry(always_fails)
        
        # Check delays are increasing
        delays = result['retry_delays']
        assert len(delays) == 2  # 2 delays for 3 attempts
        assert delays[1] > delays[0]
    
    def test_conditional_retry(self):
        """Test conditional retry based on error type"""
        retry = RetryStrategy(max_retries=3, initial_delay=0.1)
        
        def should_retry(error):
            return isinstance(error, ValueError)
        
        def non_retryable_error():
            raise TypeError("Should not retry")
        
        result = retry.execute_with_conditional_retry(
            non_retryable_error,
            should_retry
        )
        
        assert result['success'] == False
        assert result['attempts'] == 1  # Should stop immediately
        assert result['skipped_retries'] == 2


class TestPlaywrightRetryStrategy:
    """Test Playwright-specific retry logic"""
    
    def test_timeout_error_retryable(self):
        """Test TimeoutError is retryable"""
        retry = PlaywrightRetryStrategy(max_retries=3)
        
        timeout_error = Exception("TimeoutError: Navigation timeout")
        
        assert retry.should_retry_playwright_error(timeout_error) == True
    
    def test_syntax_error_not_retryable(self):
        """Test SyntaxError is not retryable"""
        retry = PlaywrightRetryStrategy(max_retries=3)
        
        syntax_error = SyntaxError("Invalid syntax")
        
        assert retry.should_retry_playwright_error(syntax_error) == False
    
    def test_network_error_retryable(self):
        """Test network errors are retryable"""
        retry = PlaywrightRetryStrategy(max_retries=3)
        
        network_error = Exception("NetworkError: Connection refused")
        
        assert retry.should_retry_playwright_error(network_error) == True


class TestErrorHandler:
    """Test error handling and recovery"""
    
    def test_handle_error_basic(self):
        """Test basic error handling"""
        handler = ErrorHandler()
        
        try:
            raise ValueError("Test error")
        except Exception as e:
            error_info = handler.handle_error(e)
        
        assert error_info['error_type'] == 'ValueError'
        assert error_info['error_message'] == 'Test error'
        assert 'traceback' in error_info
        assert 'severity' in error_info
    
    def test_assess_severity(self):
        """Test error severity assessment"""
        handler = ErrorHandler()
        
        # Critical error
        try:
            raise Exception("Fatal system error")
        except Exception as e:
            info = handler.handle_error(e)
            assert info['severity'] == 'critical'
        
        # Medium error
        try:
            raise Exception("Timeout exceeded")
        except Exception as e:
            info = handler.handle_error(e)
            assert info['severity'] == 'medium'
    
    def test_is_recoverable(self):
        """Test determining if error is recoverable"""
        handler = ErrorHandler()
        
        # Recoverable
        try:
            raise Exception("Timeout error")
        except Exception as e:
            info = handler.handle_error(e)
            assert info['recoverable'] == True
        
        # Non-recoverable
        try:
            raise SyntaxError("Invalid syntax")
        except Exception as e:
            info = handler.handle_error(e)
            assert info['recoverable'] == False
    
    def test_recovery_suggestions(self):
        """Test recovery suggestions are provided"""
        handler = ErrorHandler()
        
        try:
            raise Exception("Element not found")
        except Exception as e:
            info = handler.handle_error(e)
            
            assert len(info['recovery_suggestions']) > 0
            assert any('selector' in s.lower() for s in info['recovery_suggestions'])
    
    def test_register_custom_strategy(self):
        """Test registering custom recovery strategy"""
        handler = ErrorHandler()
        
        handler.register_recovery_strategy(
            "CustomError",
            ["Try solution 1", "Try solution 2"]
        )
        
        try:
            raise Exception("CustomError occurred")
        except Exception as e:
            info = handler.handle_error(e)
            
            assert "Try solution 1" in info['recovery_suggestions']
    
    def test_error_summary(self):
        """Test error summary generation"""
        handler = ErrorHandler()
        
        # Generate some errors
        for i in range(5):
            try:
                if i % 2 == 0:
                    raise ValueError("Even error")
                else:
                    raise TypeError("Odd error")
            except Exception as e:
                handler.handle_error(e)
        
        summary = handler.get_error_summary()
        
        assert summary['total_errors'] == 5
        assert 'ValueError' in summary['by_type']
        assert 'TypeError' in summary['by_type']


class TestDOMMapper:
    """Test DOM mapping and selector strategies"""
    
    def test_generate_selector_strategies(self):
        """Test generating multiple selector strategies"""
        mapper = DOMMapper()
        
        strategies = mapper._generate_selector_strategies(
            "click the submit button",
            primary_selector="#submit"
        )
        
        assert len(strategies) > 0
        assert strategies[0][0] == "Primary Selector"
        assert strategies[0][1] == "#submit"
    
    def test_button_selector_strategies(self):
        """Test button-specific strategies"""
        mapper = DOMMapper()
        
        strategies = mapper._generate_selector_strategies(
            "click the submit button"
        )
        
        # Should include button-specific selectors
        selectors = [s[1] for s in strategies]
        assert any('button' in sel for sel in selectors)
        assert any('submit' in sel for sel in selectors)
    
    def test_input_selector_strategies(self):
        """Test input field strategies"""
        mapper = DOMMapper()
        
        strategies = mapper._generate_selector_strategies(
            "enter email in the email field"
        )
        
        selectors = [s[1] for s in strategies]
        assert any('email' in sel for sel in selectors)
        assert any('input' in sel for sel in selectors)
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        mapper = DOMMapper()
        
        keywords = mapper._extract_keywords("Click the blue submit button")
        
        assert 'click' in keywords
        assert 'blue' in keywords
        assert 'submit' in keywords
        assert 'button' in keywords
    
    def test_generate_smart_selector(self):
        """Test smart selector generation"""
        mapper = DOMMapper()
        
        # With ID (highest priority)
        selector = mapper.generate_smart_selector("button", {
            "id": "submit-btn",
            "class": "btn btn-primary",
            "type": "submit"
        })
        assert selector == "#submit-btn"
        
        # With class (no ID)
        selector = mapper.generate_smart_selector("button", {
            "class": "btn btn-primary",
            "type": "submit"
        })
        assert selector == "button.btn"
    
    def test_suggest_alternatives(self):
        """Test suggesting alternative selectors"""
        mapper = DOMMapper()
        
        # ID selector alternatives
        alternatives = mapper.suggest_alternative_selectors("#submit-btn")
        
        assert len(alternatives) > 0
        assert any("submit-btn" in alt for alt in alternatives)
    
    def test_successful_selector_logging(self):
        """Test logging successful selectors"""
        mapper = DOMMapper()
        
        mapper._log_successful_selector(
            "click submit button",
            "#submit",
            "ID Selector"
        )
        
        key = "click submit button:#submit"
        assert key in mapper.successful_selectors
        assert mapper.successful_selectors[key]['success_count'] == 1
    
    def test_get_best_selector(self):
        """Test retrieving best selector"""
        mapper = DOMMapper()
        
        # Log multiple successful selectors
        mapper._log_successful_selector("click button", "#btn1", "Strategy1")
        mapper._log_successful_selector("click button", "#btn1", "Strategy1")
        mapper._log_successful_selector("click button", "#btn2", "Strategy2")
        
        best = mapper.get_best_selector("click button")
        
        assert best == "#btn1"  # Used twice


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])