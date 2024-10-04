from dataclasses import dataclass, field
from socket import gethostname
from typing import Any, Dict, List, Optional

from shillelagh.backends.apsw.db import DEFAULT_SCHEMA

from dbt.contracts.connection import Credentials
from dbt.dataclass_schema import dbtClassMixin


@dataclass
class ShillelaghAdapterConfig(dbtClassMixin):
    name: str
    fully_qualified_class_name: Optional[str] = None
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ShillelaghCredentials(Credentials):
    database: str = ":memory:"
    schema: str = DEFAULT_SCHEMA
    safe_mode: bool = True
    adapters: List[ShillelaghAdapterConfig] = field(default_factory=list)

    @property
    def type(self):
        return "shillelagh"

    @property
    def unique_field(self):
        """
        Hashed and included in anonymous telemetry to track adapter adoption.
        Pick a field that can uniquely identify one team/organization building with this adapter
        """
        return gethostname()

    def _connection_keys(self):
        return ("database", "schema", "safe_mode", "adapters")
