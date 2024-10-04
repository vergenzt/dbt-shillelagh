from ...include.shillelagh import PACKAGE_PATH as INCLUDE_PACKAGE_PATH
from .credentials import ShillelaghCredentials
from .impl import ShillelaghAdapter

from dbt.adapters.base.plugin import AdapterPlugin

Plugin = AdapterPlugin(
    adapter=ShillelaghAdapter,
    credentials=ShillelaghCredentials,
    include_path=INCLUDE_PACKAGE_PATH,
    dependencies=["sqlite"],
)
