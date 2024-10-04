import traceback
from typing import cast

from contextlib import contextmanager

from shillelagh.adapters.registry import registry
from shillelagh.backends.apsw.db import connect
from shillelagh.backends.apsw.db import Connection as ShillelaghConnection
from shillelagh.backends.apsw.db import Cursor as ShillelaghCursor
from shillelagh.exceptions import Error as ShillelaghError

from dbt.adapters.sql.connections import SQLConnectionManager
from dbt.contracts.connection import (
    AdapterResponse,
    Connection,
    ConnectionState,
)
from dbt.events.adapter_endpoint import AdapterLogger
from dbt.exceptions import DbtRuntimeError

from .credentials import ShillelaghCredentials


logger = AdapterLogger("Shillelagh")


class ShillelaghConnectionManager(SQLConnectionManager):
    TYPE = "shillelagh"

    @contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except DbtRuntimeError:
            raise
        except ShillelaghError as e:
            self.release()
            logger.info("shillelagh error: {}".format(e))
            logger.debug("\n" + "\n".join(traceback.format_tb(e.__traceback__)))
        except Exception as e:
            logger.debug("Error running SQL: {}".format(e))
            logger.debug("Rolling back transaction.")
            raise DbtRuntimeError(str(e)).with_traceback(e.__traceback__) from e

    @classmethod
    def open(cls, connection: Connection) -> Connection:
        if connection.state == ConnectionState.OPEN:
            logger.debug("Connection is already open, skipping open.")
            return connection

        assert (credentials := cast(ShillelaghCredentials, connection.credentials))

        for adapter_cfg in credentials.adapters:
            if fqcn := adapter_cfg.fully_qualified_class_name:
                modulepath, _, classname = fqcn.rpartition(':')
                registry.register(adapter_cfg.name, modulepath, classname)

        adapter_names = [ adapter.name for adapter in credentials.adapters ]
        adapter_kwargs = {
            adapter.name: adapter.kwargs for adapter in credentials.adapters 
            if adapter.kwargs is not None
        }

        handle = connect(
            path=credentials.database,
            adapters=adapter_names,
            adapter_kwargs=adapter_kwargs,
            safe=credentials.safe_mode,
            schema=credentials.schema,
        )

        connection.handle = handle
        connection.state = ConnectionState.OPEN
        return connection

    @classmethod
    def get_response(cls, cursor: ShillelaghCursor) -> AdapterResponse:
        return AdapterResponse("OK", rows_affected=cursor.rowcount)

    def cancel(self, connection: Connection):
        handle = cast(ShillelaghConnection, connection.handle)
        handle._connection.interrupt()
