from typing import Optional

from ai.query_parser import parse_query
from ai.schemas import QueryResult


def understand_query(
    message: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
) -> QueryResult:
    """
    Main interface for the query-understanding module.

    The natural-language message is processed by the AI parser.
    GPS coordinates are supplied separately by the application.
    """

    result = parse_query(message)

    result.latitude = latitude
    result.longitude = longitude

    return result