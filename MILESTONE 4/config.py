

import os
from pathlib import Path


class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0'))
    
    # Test execution settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    INITIAL_RETRY_DELAY = float(os.getenv('INITIAL_RETRY_DELAY', '1.0'))
    BACKOFF_FACTOR = float(os.getenv('BACKOFF_FACTOR', '2.0'))
    TEST_TIMEOUT = int(os.getenv('TEST_TIMEOUT', '60'))
    
    # Browser settings
    HEADLESS = os.getenv('HEADLESS', 'True').lower() == 'true'
    BROWSER_TYPE = os.getenv('BROWSER_TYPE', 'chromium')  # chromium, firefox, webkit
    VIEWPORT_WIDTH = int(os.getenv('VIEWPORT_WIDTH', '1920'))
    VIEWPORT_HEIGHT = int(os.getenv('VIEWPORT_HEIGHT', '1080'))
    
    # Screenshot settings
    SCREENSHOT_QUALITY = int(os.getenv('SCREENSHOT_QUALITY', '80'))
    SCREENSHOT_FULL_PAGE = os.getenv('SCREENSHOT_FULL_PAGE', 'True').lower() == 'true'
    
    # Output settings
    OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', './outputs'))
    SCREENSHOTS_DIR = OUTPUT_DIR / 'screenshots'
    REPORTS_DIR = OUTPUT_DIR / 'reports'
    HTML_REPORTS_DIR = OUTPUT_DIR / 'html_reports'
    TEST_SCRIPTS_DIR = OUTPUT_DIR / 'test_scripts'
    
    # History settings
    HISTORY_LIMIT = int(os.getenv('HISTORY_LIMIT', '100'))
    AUTO_CLEANUP_DAYS = int(os.getenv('AUTO_CLEANUP_DAYS', '30'))
    
    # Performance settings
    MAX_CONCURRENT_TESTS = int(os.getenv('MAX_CONCURRENT_TESTS', '3'))
    ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'True').lower() == 'true'
    
    # Feature flags
    ENABLE_WEB_SEARCH = os.getenv('ENABLE_WEB_SEARCH', 'False').lower() == 'true'
    ENABLE_REAL_TIME_UPDATES = os.getenv('ENABLE_REAL_TIME_UPDATES', 'True').lower() == 'true'
    ENABLE_ANALYTICS = os.getenv('ENABLE_ANALYTICS', 'True').lower() == 'true'
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'outputs/app.log')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])