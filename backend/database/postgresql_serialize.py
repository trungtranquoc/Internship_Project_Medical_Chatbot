from typing import Any, Dict, List
import uuid
from datetime import datetime

def serialize_db_row(row: Any) -> Dict[str, Any]:
    """
    Convert database row objects to JSON serializable format.
    Handles UUID, datetime, and other non-serializable types.
    """
    if row is None:
        return None
    
    # Convert Row object to dict first
    if hasattr(row, '_asdict'):
        data = row._asdict()
    elif hasattr(row, 'keys'):
        data = dict(row)
    else:
        data = row
    
    # Recursively serialize all values
    def serialize_value(value):
        if isinstance(value, uuid.UUID):
            return str(value)
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, dict):
            return {k: serialize_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return [serialize_value(item) for item in value]
        else:
            return value
    
    return {key: serialize_value(value) for key, value in data.items()}

def serialize_db_rows(rows: List[Any]) -> List[Dict[str, Any]]:
    """
    Serialize a list of database rows.
    """
    return [serialize_db_row(row) for row in rows]