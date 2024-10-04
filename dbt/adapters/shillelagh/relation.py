from dataclasses import dataclass, field

from dbt.adapters.base.relation import BaseRelation, Policy


@dataclass
class ShillelaghQuotePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = True


@dataclass
class ShillelaghIncludePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = True


@dataclass(frozen=True, eq=False, repr=False)
class ShillelaghRelation(BaseRelation):
    quote_policy: ShillelaghQuotePolicy = field(default_factory=ShillelaghQuotePolicy)
    include_policy: ShillelaghIncludePolicy = field(default_factory=ShillelaghIncludePolicy)
