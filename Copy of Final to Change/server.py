import socket
from _thread import *
import pickle
import ObjClasses as obj
from GameProjectOrganized import Game


server = "192.168.1.145"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}


idCount = 0



def threaded_client(conn, p, gameID):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameID in games:
                game = games[gameID]
                players = obj.players
                reply = game
                

                if not data:
                    break
                else:
                    if data == "start":
                        games[gameID].ready = True
                    elif data == "isStart":
                        reply = games[gameID].ready
                    elif data == "players":
                        reply = players
                    elif data == "cards":
                        reply = players[p].cards
                    elif data == "reset":
                        for i in range(len(players)):
                            Game.reset(players[i])
                            Game.initialization(players[i])
                    elif data == "add":
                        obj.players.append(obj.Player(("player" + str(p)), [], 0, 0, 1000, 0))
                    elif data == "initial":
                        Game.initialization(players[p])
                        reply = players
                    elif data == "hit":
                        Game.hit(players[p])
                    elif data == "stand":
                        Game.stand(players[p])
                        if Game.allStand(players) == False:
                            reply = "wait"
                        else:
                            Game.finalStand(players[0], players[p])
                            reply = "done"
                    elif data == "bust":
                        Game.stand(players[p])
                        players[p].bust = True
                        if Game.allStand(players) == False:
                            reply = "wait"
                        else:
                            Game.finalStand(players[0], players[p])
                            reply = "done"
                    elif data == "split":
                        Game.split(players[p])
                    elif data != "get":
                        data = int(float(data))
                        bets = players[p].chips - data
                        players[p].chips = data
                        players[p].bet = bets
                                
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except socket.error as e:
            print(e)
            break

    print("Lost connection")
    try:
        del games[gameID]
        print("Closing Game", gameID)
        while (len(obj.players) != 0):
            del obj.players[0]
            
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)


    idCount += 1
    gameID = 0
    if idCount == 1:
        games[gameID] = Game(gameID)
        print("Creating a new game...")
        obj.players.append(obj.Player(("dealer"), [], 0, 0, 0, 0))
        Game.initialization(obj.players[0])
    elif idCount == 5:
        games[gameID].ready = True

    

    start_new_thread(threaded_client, (conn, idCount, gameID))
