# Менеджер виртуальных машин на сокетах. Клиент-серверное приложение 

---

```bash
git clone ... && cd socket-vm_manager
```

## Запуск сервера:

```bash
sudo docker compose up
```

## Запуск клиента:

**build image**:
```bash
sudo docker build -t vmclient client/
```

**run container**:
```bash
sudo docker run -it -e "HOST=0.0.0.0" -e "PORT=8080" --network host vmclient
```
