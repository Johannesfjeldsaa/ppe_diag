from dataclasses import dataclass

from ppe_diag.scripts.utils.base_config import BaseConfig

@dataclass
class main_config(BaseConfig):



@dataclass
class checked_main_config(main_config):
    """Checked version of main_config with additional/processed validation."""
    pass