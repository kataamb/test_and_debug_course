# queries/sql_types.py
from __future__ import annotations
from typing import Tuple, Dict
from decimal import Decimal
from datetime import date, time, datetime
from uuid import UUID
from sqlalchemy.sql.elements import TextClause

SqlParam = int | float | Decimal | str | bool | datetime | date | time | UUID | None
SqlParams = Dict[str, SqlParam]
TextAndParams = Tuple[TextClause, SqlParams]