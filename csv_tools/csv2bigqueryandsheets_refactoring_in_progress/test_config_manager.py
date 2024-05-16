# test_config_manager.py
from your_module.config_manager import ConfigManager
import os

def test_config_manager():
    os.environ['PROJECT_ID'] = 'test_project'
    config = ConfigManager()
    assert config.project_id == 'test_project'
    # Add more assertions for each configuration item