from dataclasses import dataclass

@dataclass
class TestConfig:
    headed: bool = True
    slowmo: int = 0
    screenshot: str = "off"   # off | on | only-on-failure
    video: bool = False
