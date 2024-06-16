import asyncio
import json
import logging
import traceback

from database.db import Database
from server import models


class Server:
    def __init__(self, host: str, port: int, db_uri: str):
        self.host = host
        self.port = port
        self.db_uri = db_uri
        self.logger = logging.getLogger("server")
        self.vms: dict[str, int] = {}

    async def start(self):
        self.logger.info(f"Starting server on {self.host}:{self.port}...")
        self.db = Database(self.db_uri)
        await self.db.connect()
        server = await asyncio.start_server(self.handle_client, self.host, self.port)

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername = writer.get_extra_info("peername")
        self.logger.info(f"New client connection from {peername}")

        while True:
            try:
                data = await reader.readline()
                data = data.decode().strip()
                self.logger.info(f"Received data: {data}")
                if not data:
                    break
                request = json.loads(data)
                response = await self.process_request(request, peername)
                writer.write(json.dumps(response).encode() + b"\n")
                await writer.drain()
            except Exception as e:
                traceback.print_exc()
                self.logger.error(f"Error processing request: {e}")
                break

        self.logger.info(f"Client connection from {peername} closed")
        writer.close()

    async def process_request(self, request: dict, peername: str):
        command = request.get("command")
        data = request.get("data")
        vm_id = self.vms.get(peername)

        self.logger.info(f"{command = }\n{data = }\n{vm_id = }")
        if command == "auth":
            return await self.authenticate(data, peername)
        elif command == "register":
            return await self.register_vm(data)
        elif command == "list_vms":
            return await self.list_vms()
        elif command == "list_authorized_vms":
            return await self.list_authorized_vms()
        elif command == "logout":
            return await self.logout(peername)
        elif command == "update":
            return await self.update_vm(vm_id, data)
        elif command == "list_disks":
            return await self.list_disks()
        else:
            return {"error": "Invalid command"}

    async def authenticate(self, data: dict, peername: str) -> dict:
        vm_id = data.get("vm_id")
        password = data.get("password")

        if not vm_id or not password:
            return {"error": "Missing credentials"}

        is_password_valid = await self.db.check_password(vm_id, password)
        if not is_password_valid:
            return {"error": "Invalid credentials"}

        self.vms[peername] = vm_id
        self.logger.info(f"VM {vm_id} authenticated")
        return {"success": True}

    async def register_vm(self, data: dict) -> dict:
        try:
            vm = models.VMRequestModel(**data)
            vm_id = await self.db.add_vm(vm)
            self.logger.info(f"VM {vm_id} registered")
            return {"success": True, "vm_id": vm_id}
        except Exception as e:
            self.logger.error(f"Error registering VM: {e}")
            return {"error": "Failed to register VM"}

    async def list_vms(self) -> dict | None:
        vms = await self.db.get_vms_list()
        if vms:
            vms = models.VMsList(vms=vms)
            return vms.model_dump()

    async def list_authorized_vms(self) -> str | None:
        authorized_vms_ids = list(self.vms.values())
        vms = await self.db.get_vms_list(vms_ids=authorized_vms_ids)  
        if vms:
            vms = models.VMsList(vms=vms)
            return vms.model_dump_json()

    async def logout(self, peername: str) -> bool | dict:
        vm = self.vms.pop(peername, None)
        if vm:
            self.logger.info(f"VM {peername} logged out")
            return {"success": True}
        return {"error": "You have not been logged in"}
        
    async def update_vm(self, vm_id: int, data: dict) -> dict:
        if await self.db.update_vm(vm_id, data):
            self.logger.info(f"VM {vm_id} updated")
            return {"success": True}
        return {"success": False}

    async def list_disks(self) -> str | None:
        disks = await self.db.get_disks_list()
        if disks:
            disks = models.DisksList(disks=disks)
            return disks.model_dump_json()

