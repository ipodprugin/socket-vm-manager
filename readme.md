# Менеджер виртуальных машин на сокетах. Клиент-серверное приложение 

---

```bash
git clone https://github.com/ipodprugin/socket-vm-manager.git && cd socket-vm-manager
cp example.env .env
```

## Запуск сервера:

```bash
docker compose up
```

## Запуск клиента:

**build image**:
```bash
docker build -t vmclient client/
```

**run container**:
```bash
docker run -it -e "HOST=0.0.0.0" -e "PORT=8080" --network host vmclient
```
