# scripts/create_admin.py

import asyncio
from models.user import Role
import services.auth as service


async def main():
    user = await service.add_user(
        username="admin", email="admin@mail.com", password="123456", role=Role.admin
    )

    print(f"Admin created: {user.username}")


if __name__ == "__main__":
    asyncio.run(main())
