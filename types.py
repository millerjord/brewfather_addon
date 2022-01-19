from datetime import datetime
from typing import Optional

from typing_extensions import TypedDict


class Batch(TypedDict):
    batch_id: str
    batchNo: int
    BeerName: str
    brewDate: datetime
    sg: float
    temp: float
    timestamp: datetime
