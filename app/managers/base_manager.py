from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from supabase import Client

from app.utils.supabase import get_supabase_client

T = TypeVar("T")


class BaseManager(Generic[T]):
    """Base manager class for Supabase operations."""

    def __init__(self, table_name: str):
        self.client: Client = get_supabase_client()
        self.table_name = table_name

    async def get_by_id(self, id: UUID) -> Optional[Dict[str, Any]]:
        """Get a record by ID."""
        result = (
            self.client.table(self.table_name).select("*").eq("id", str(id)).execute()
        )
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None

    async def get_many(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Get multiple records with optional filtering."""
        query = (
            self.client.table(self.table_name).select("*").limit(limit).offset(offset)
        )

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        result = query.execute()
        return result.data if result.data else []

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record."""
        result = self.client.table(self.table_name).insert(data).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        return {}

    async def update(self, id: UUID, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing record."""
        result = (
            self.client.table(self.table_name).update(data).eq("id", str(id)).execute()
        )
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None

    async def delete(self, id: UUID) -> bool:
        """Delete a record by ID."""
        result = self.client.table(self.table_name).delete().eq("id", str(id)).execute()
        return bool(result.data)
