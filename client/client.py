import asyncio
import json
import logging

logging.basicConfig(level=logging.INFO)


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.logger = logging.getLogger("client")

    async def connect(self):
        self.logger.info(f"Connecting to server {self.host}:{self.port}")
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        # self.reader, self.writer = await asyncio.open_connection(host=f"ws://{self.host}:{self.port}")

    async def send_request(self, request: dict) -> dict | None:
        self.logger.info(f"Sending request: {request}")
        self.writer.write(json.dumps(request).encode() + b"\n")
        await self.writer.drain()
        response = await self.reader.readline()
        response = response.decode().strip()
        try:
            return json.loads(response)
        except json.decoder.JSONDecodeError:
            self.logger.error(f"Empty response on request: {request}")

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    async def authenticate(self, vm_id: int, password: str):
        request = {"command": "auth", "data": {"vm_id": vm_id, "password": password}}
        response = await self.send_request(request)
        return response

    async def register(self, data: dict):
        request = {"command": "register", "data": data}
        response = await self.send_request(request)
        return response

    async def list_vms(self):
        request = {"command": "list_vms"}
        response = await self.send_request(request)
        return response

    async def list_authorized_vms(self):
        request = {"command": "list_authorized_vms"}
        response = await self.send_request(request)
        return response

    async def logout(self):
        request = {"command": "logout"}
        response = await self.send_request(request)
        return response

    async def update(self, data: dict):
        request = {"command": "update", "data": data}
        response = await self.send_request(request)
        return response

    async def list_disks(self):
        request = {"command": "list_disks"}
        response = await self.send_request(request)
        return response


async def main():
    from config import settings


    client = Client(host=settings.HOST, port=settings.PORT)
    await client.connect()

    command = input("Нажмите Enter для выполнения функций, или q для выхода: ")
    if command != "q":
        # Пример регистрации
        new_vm_data = {"ram": 8, "cpu": 2, "password": "password", "disks": [{"size": 10}]}
        response = await client.register(new_vm_data)
        print(f"Registration response: {response}\n")
        vm_id = response.get("vm_id")

        input()
        # Пример авторизации
        response = await client.authenticate(vm_id=vm_id, password="password")
        print(f"Auth response: {response}\n")

        input()
        # Вывод всех виртуальных машин
        response = await client.list_vms()
        print(f"List VMs response: {response}\n")

        input()
        # Вывод подключенных виртуальных машин
        response = await client.list_authorized_vms()
        print(f"List authorized VMs response: {response}\n")

        input()
        # Вывод дисков
        response = await client.list_disks()
        print(f"List disks response: {response}\n")

        input()
        # Изменение данных виртуальной машины
        update_vm_data = {"id": vm_id, "ram": 4, "cpu": 6}
        response = await client.update(update_vm_data)
        print(f"Update vm response: {response}\n")

        input()
        # Logout
        response = await client.logout()
        print(f"Logout response: {response}\n")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

