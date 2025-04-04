#!/usr/bin/env python
"""
Interactive REPL for testing managers and services.
Usage:
    railway run poetry run python scripts/repl.py

This will drop you into an iPython shell with all managers and services pre-imported
and an asyncio event loop ready to go.
"""
import asyncio
import os
from uuid import UUID

import IPython
import nest_asyncio
from traitlets.config import Config

# Set up environment
os.environ["PYTHONASYNCIODEBUG"] = "1"

# Import all managers and services
from app.managers.user_manager import UserManager
from app.managers.organization_manager import OrganizationManager
from app.managers.clerk_manager import ClerkManager
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


async def _async_main():
    """Create instances of managers and services for testing."""
    # Initialize managers and services
    user_manager = UserManager()
    org_manager = OrganizationManager()
    clerk_manager = ClerkManager()
    user_service = UserService()

    # Example test data
    test_user_id = (
        "user_2cRNVPSDaWoQHYKf1bXYGrwCRg1"  # Replace with a real Clerk user ID
    )
    test_org_id = UUID(
        "123e4567-e89b-12d3-a456-426614174000"
    )  # Replace with a real org ID

    # Return a dict of objects to expose in the REPL
    return {
        # Managers
        "user_manager": user_manager,
        "org_manager": org_manager,
        "clerk_manager": clerk_manager,
        # Services
        "user_service": user_service,
        # Test data
        "test_user_id": test_user_id,
        "test_org_id": test_org_id,
        # Schemas
        "UserCreate": UserCreate,
        "UserUpdate": UserUpdate,
        "OrganizationCreate": OrganizationCreate,
        "OrganizationUpdate": OrganizationUpdate,
    }


def get_ipython_config():
    """Configure IPython shell."""
    c = Config()
    c.InteractiveShellApp.exec_lines = [
        "import asyncio",
        "from uuid import UUID",
        # Add any other imports you commonly need
    ]
    return c


def main():
    """Start the REPL with our context."""
    # Set up asyncio for interactive use
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    nest_asyncio.apply()

    # Get async context
    context = asyncio.run(_async_main())

    # Create banner with usage instructions
    banner = """
🔧 Accountable API Development Shell 🔧
=====================================

Available objects:
- Managers: user_manager, org_manager, clerk_manager
- Services: user_service
- Test Data: test_user_id, test_org_id
- Schemas: UserCreate, UserUpdate, OrganizationCreate, OrganizationUpdate

Helper Functions:
- await_it(coro): Run a coroutine in the event loop
- async_run(coro): Alternative async runner that creates a new event loop

Example usage:
    # Get a user using the service
    user = await_it(user_service.get_current_user(test_user_id))
    
    # Get a user directly from the manager
    user = await_it(user_manager.get_user_by_clerk_id(test_user_id))
    
    # Create an organization
    org = await_it(org_manager.create_organization(
        OrganizationCreate(name="Test Org", slug="test-org"),
        UUID(test_user_id)
    ))

    # Alternative async runner if await_it fails
    user = async_run(user_service.get_current_user(test_user_id))
"""

    # Create helper functions for running coroutines
    def await_it(coro):
        """Helper to run coroutines in the REPL."""
        return asyncio.get_event_loop().run_until_complete(coro)

    def async_run(coro):
        """Alternative helper that creates a new event loop."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    # Add helpers to context
    context["await_it"] = await_it
    context["async_run"] = async_run

    # Start IPython shell
    IPython.start_ipython(
        argv=[],
        user_ns=context,
        config=get_ipython_config(),
        banner1=banner,
    )


if __name__ == "__main__":
    main()
