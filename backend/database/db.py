import asyncpg
from typing import Optional

from server import models


class Database:
    def __init__(self, db_rui: str):
        self.db_rui = db_rui

    async def connect(self):
        self.conn = await asyncpg.connect(dsn=self.db_rui)

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def add_vm(self, vm: models.VMRequestModel) -> int:
        async with self.conn.transaction():
            vm_id = await self.conn.fetchval(
                """
                INSERT INTO vms (ram, cpu, password)
                VALUES ($1, $2, crypt($3, gen_salt('md5')))
                RETURNING id
                """,
                vm.ram,
                vm.cpu,
                vm.password,
            )
            for disk in vm.disks:
                await self.conn.execute(
                    """
                    INSERT INTO disks (size, vm_id)
                    VALUES ($1, $2)
                    """,
                    disk.size,
                    vm_id,
                )
            return vm_id

    async def check_password(self, vm_id: str, password: str) -> bool | None:
        is_password_valid = await self.conn.fetchval(
            """
            SELECT (password = crypt($1, password)) 
            AS password_match
            FROM vms
            WHERE id = $2;
            """,
            password,
            vm_id,
        )
        return is_password_valid

    async def get_vms_list(self, vms_ids: Optional[list[int]] = None) -> list[models.VMResponseModel] | None:
        if vms_ids:
            vms = await self.conn.fetch(
                """
                SELECT * FROM vms WHERE id = ANY($1::int[])
                """,
                vms_ids,
            )
        else:
            vms = await self.conn.fetch("SELECT * FROM vms")
        if not vms:
            return None

        for vm_id, vm in enumerate(vms):
            _vm = models.VMResponseModel(**vm)
            disks = await self.conn.fetch(
                """
                SELECT * FROM disks WHERE vm_id = $1
                """,
                _vm.id,
            )
            for disk_id, disk_row in enumerate(disks):
                disks[disk_id] = models.DiskDBModel(**disk_row)
            _vm.disks = disks
            vms[vm_id] = _vm
        return vms

    async def update_vm(self, vm_id: int, data: dict) -> int:
        async with self.conn.transaction():
            update_fields = ", ".join(
                [
                    f"password = crypt(${i + 1}, gen_salt('md5'))" if column == "password" 
                    else f"{column} = ${i + 1}" 
                    for i, column in enumerate(data)
                ]
            )
            await self.conn.execute(
                f"""
                update vms 
                set {update_fields}
                where id = {vm_id}
                """,
                *data.values(),
            )
            return True

    async def get_disks_list(self) -> list[models.DiskResponseModel] | None:
        disks = await self.conn.fetch(
            """
            SELECT d.*, v.ram, v.cpu
            FROM disks d
            LEFT JOIN vms v ON v.id = d.vm_id;
            """
        )
        if not disks:
            return None
        for index, disk in enumerate(disks):
            disks[index] = models.DiskResponseModel(**disk)
        return disks

