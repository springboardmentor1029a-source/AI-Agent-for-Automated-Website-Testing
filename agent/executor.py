"""
Test Executor Module
Executes generated Playwright scripts and captures results
"""

import subprocess
import json
import os
import tempfile
from typing import Dict

class TestExecutor:
    """Executes Playwright test scripts and captures results"""
    
    def execute(self, script_code: str) -> Dict:
        """
        Execute the generated Playwright script
        
        Args:
            script_code: Python script code to execute
            
        Returns:
            Dictionary containing test results
        """
        # Create temporary file for the script with UTF-8 encoding
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script_code)
            script_path = f.name
        
        try:
            # Execute the script (longer timeout for visible browser)
            result = subprocess.run(
                ['python', '-X', 'utf8', script_path],
                capture_output=True,
                text=True,
                timeout=120,
                encoding='utf-8'
            )
            
            # Parse the output
            if result.returncode == 0:
                try:
                    output = json.loads(result.stdout)
                    return {
                        'status': 'success',
                        'results': output,
                        'stdout': result.stdout,
                        'stderr': result.stderr
                    }
                except json.JSONDecodeError:
                    return {
                        'status': 'error',
                        'error': 'Failed to parse test output',
                        'stdout': result.stdout,
                        'stderr': result.stderr
                    }
            else:
                return {
                    'status': 'error',
                    'error': f'Script execution failed with code {result.returncode}',
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
        
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'error': 'Test execution timed out after 60 seconds'
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'error': f'Execution error: {str(e)}'
            }
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(script_path)
            except:
                pass
    
    def validate_script(self, script_code: str) -> Dict:
        """
        Validate the generated script for syntax errors
        
        Args:
            script_code: Python script code to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            compile(script_code, '<string>', 'exec')
            return {
                'valid': True,
                'errors': []
            }
        except SyntaxError as e:
            return {
                'valid': False,
                'errors': [f'Syntax error at line {e.lineno}: {e.msg}']
            }
        except Exception as e:
            return {
                'valid': False,
                'errors': [f'Validation error: {str(e)}']
            }
