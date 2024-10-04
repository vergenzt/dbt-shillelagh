from dbt.adapters.base.meta import available
from dbt.adapters.sqlite.impl import SQLiteAdapter

from .connections import ShillelaghConnectionManager
from .relation import ShillelaghRelation


class ShillelaghAdapter(SQLiteAdapter):
    ConnectionManager = ShillelaghConnectionManager  # type: ignore
    Relation = ShillelaghRelation  # type: ignore

    @available
    def target_path(self):
        breakpoint()
        return self.config.target_path
