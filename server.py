from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock
import pickle
import random
import time

WIDTH, HEIGHT = 800, 600
CELL = 50
zone_up = WIDTH // CELL
zone_down = HEIGHT // CELL
stop = True

game_data = {
    "players": {},
    "apple": [random.randint(0, zone_up - 1) * CELL,
              random.randint(0, zone_down - 1) * CELL]
}

clients = []
lock = Lock()

def spawn_apple():
    return [random.randint(0, zone_up - 1) * CELL,
            random.randint(0, zone_down - 1) * CELL]

def handle_client(conn, player_id):
    global game_data
    print(f"{player_id} підключився")

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            player_state = pickle.loads(data)

            with lock:
                if player_id not in game_data["players"]:
                    continue

                pdata = game_data["players"][player_id]

                # напрямок від клієнта
                if "direction" in player_state:
                    pdata["direction"] = player_state["direction"]
                    
                if "name" in player_state:
                    pdata["name"] = player_state["name"]

                # рух
                if pdata["direction"] == "left":
                    pdata["x"] -= CELL
                elif pdata["direction"] == "right":
                    pdata["x"] += CELL
                elif pdata["direction"] == "up":
                    pdata["y"] -= CELL
                elif pdata["direction"] == "down":
                    pdata["y"] += CELL
                    
                # межі
                if (
                    pdata["x"] < 0
                    or pdata["x"] >= WIDTH
                    or pdata["y"] < 0
                    or pdata["y"] >= HEIGHT
                ):
                    print(player_id, "врізався в стіну")

                    game_data["winner"] = (
                        "player1" if player_id == "player2" else "player2"
                    )
                
                # перевірка зіткнень з хвостами всіх гравців
                for other_id, other_data in game_data["players"].items():
                    if other_id == player_id:
                        # перевірка власного хвоста
                        if (pdata["x"], pdata["y"]) in other_data["tail"]:
                            print(player_id, "врізався в свій хвіст")
                            game_data["winner"] = (
                                "player1" if player_id == "player2" else "player2"
                            )
                    else:
                        # зіткнення з чужим хвостом або головою
                        if (pdata["x"], pdata["y"]) in other_data["tail"] or (pdata["x"], pdata["y"]) == (other_data["x"], other_data["y"]):
                            print(player_id, "врізався в іншого гравця")
                            game_data["winner"] = other_id  # переміг той в кого врізалися

                # хвіст
                pdata["tail"].insert(0, (pdata["x"], pdata["y"]))
                if len(pdata["tail"]) > pdata["tail_length"]:
                    pdata["tail"].pop()

                # яблуко
                if pdata["x"] == game_data["apple"][0] and pdata["y"] == game_data["apple"][1]:
                    pdata["tail_length"] += 1
                    pdata["score"] += 1
                    game_data["apple"] = spawn_apple()

                    if pdata["score"] >= 10:
                        game_data["winner"] = player_id

    except:
        print(f"{player_id} відключився")

    finally:
        global stop
        with lock:
            if player_id in game_data["players"]:
                del game_data["players"][player_id]
            if conn in clients:
                clients.remove(conn)
            if len(clients) == 0: #зупинка
                    print("Сервер вимкнено")
                    stop = False
                    
        conn.close()

def broadcast_game_state():
    global stop
    while stop:
        with lock:
            for c in clients:
                try:
                    c.sendall(pickle.dumps(game_data))
                except:
                    if c in clients:
                        clients.remove(c)
        time.sleep(0.1)

# старт
sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('localhost', 8080))
sock.listen(2)
sock.settimeout(1)
print("Сервер запущено")

Thread(target=broadcast_game_state, daemon=True).start()

player_counter = 0
while stop:
    try:
        conn, addr = sock.accept()
    except:
        continue
    if player_counter >= 2:
        conn.sendall(b"FULL")
        conn.close()
        continue

    player_id = f"player{player_counter + 1}"
    player_counter += 1

    # Додаємо гравця одразу при підключенні (по різним кутам)
    with lock:
        if player_id == "player1":
            start_x = 0
            start_y = HEIGHT - CELL
            start_dir = "right"
        else:
            start_x = WIDTH - CELL
            start_y = HEIGHT - CELL
            start_dir = "left"
        game_data["players"][player_id] = {
            "x": start_x,
            "y": start_y,
            "tail": [],
            "tail_length": 0,
            "direction": start_dir,
            "score": 0,
            "name": player_id
        }

    clients.append(conn)

    # надсилання стану гри іншому гравцю
    try:
        conn.sendall(pickle.dumps(game_data))
    except:
        clients.remove(conn)

    Thread(target=handle_client, args=(conn, player_id), daemon=True).start()