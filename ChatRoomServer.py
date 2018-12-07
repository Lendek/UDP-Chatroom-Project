from socket import *
import datetime

serverPort = 5000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
activeClientsList = []

class Client:
    def __init__(self, clientAddress, userName):
        self.clientAddress = clientAddress
        self.userName = userName
        self.muteStatus = False
        self.blockedClientsList = []

def clientJoin():
    print("clientJoin called")
    userName, clientAddress = serverSocket.recvfrom(2048)
    decodedUserName = userName.decode()
#     welcomeMessage = "Welcome to the chat room " + decodedUserName + "!: ".join((str(x) for x in clientAddress))
    welcomeMessage = "Welcome to the chat room " + decodedUserName + "!: " + str(clientAddress)
    activeClientsList.append(Client(clientAddress, decodedUserName))
    if len(activeClientsList) == 1:
        serverSocket.sendto(welcomeMessage.encode(), clientAddress)
    else:
        print("send to ")
        for clients in activeClientsList:
            print(clients.userName, end=" ")
            serverSocket.sendto(welcomeMessage.encode(), clients.clientAddress)
        print()
                
def clientQuit(clientAddress):  
    print("clientQuit called")
    for clients in activeClientsList:
        goodbyeMessage = clients.userName + " has left the chat room."
        if(clients.clientAddress==clientAddress):
            activeClientsList.remove(clients)
            break
        
    serverSocket.sendto("!quit".encode(), clientAddress)
#     remove clientAddress from active users
#     send goodbye message to all active users
    for clients in activeClientsList:
        serverSocket.sendto(goodbyeMessage.encode(), clients.clientAddress)
        
def clientSend(clientAddress):
    print("clientSend called")
    for clients in activeClientsList:
        if(clients.clientAddress==clientAddress):
            modifiedMessage = clients.userName + ": " + decodedMessage
    print("Received: " + modifiedMessage)
    if len(activeClientsList) == 1:
            serverSocket.sendto("There is no one else in this chat room".encode(), clientAddress)
    else:
        for clients in activeClientsList:
#             send to all clients but self
            if(len(clients.blockedClientsList) <= 0):
                if(clients.clientAddress!=clientAddress and not clients.muteStatus):
                    serverSocket.sendto(modifiedMessage.encode(), clients.clientAddress)
                    print(clients.userName)
            else:
                if(not clients.muteStatus):
                    print("This is " + clients.userName + "'s blockList")
                    for blockedClients in range(len(clients.blockedClientsList)):
#                         do not send to clients blocking this client's clientAddress
                        print(type(clientAddress[0]), end=": ")
                        print(clientAddress[0], end=", ")
                        print(type(clientAddress[1]), end=": ")
                        print(clientAddress[1])
                        print(type(clients.blockedClientsList[blockedClients][0]), end=": ")
                        print(clients.blockedClientsList[blockedClients][0], end=", ")
                        print(type(clients.blockedClientsList[blockedClients][1]), end=": ")
                        print(clients.blockedClientsList[blockedClients][1])
                        print(type(clientAddress), end=": ")
                        print(clientAddress)
                        print(type(clients.blockedClientsList[blockedClients]), end=": ")
                        print(clients.blockedClientsList[blockedClients])
                        if(clientAddress != clients.blockedClientsList[blockedClients]):
                            serverSocket.sendto(modifiedMessage.encode(), clients.clientAddress)
                            print(clients.userName, end =" ")
                        else:
                            for blockedClient in range(len(activeClientsList)):
                                if(activeClientsList[blockedClient].clientAddress == clients.blockedClientsList[blockedClients]):
                                    print(clients.userName + " is blocking " + activeClientsList[blockedClient].userName)
        print()
        
def clientMute(clientAddress):
    print("clientMute called")
    for clients in activeClientsList:
        if(clients.clientAddress == clientAddress):
            clients.muteStatus = True
    

def clientUnmute(clientAddress):
    print("clientUnmute called")
    for clients in activeClientsList:
        if(clients.clientAddress == clientAddress):
            clients.muteStatus = False
                
def clientBlock(clientAddress):
    print("clientBlock called")
    for clients in activeClientsList:
        if(clients.clientAddress == clientAddress):
            blockedIpIndexStart = decodedMessage.find("[") + 1
            blockedIpIndexEnd = decodedMessage.find("]", blockedIpIndexStart)
            blockedPortIndexStart = decodedMessage.find("[",blockedIpIndexEnd) + 1
            blockedPortIndexEnd = decodedMessage.find("]",blockedPortIndexStart)
            blockedIpAddress = decodedMessage[blockedIpIndexStart:blockedIpIndexEnd]
            blockedPortAddress = decodedMessage[blockedPortIndexStart:blockedPortIndexEnd]
            blockedPortAddress = int(blockedPortAddress)
            blockedClientAddress = (blockedIpAddress, blockedPortAddress)
            clients.blockedClientsList.append(blockedClientAddress)
            print(clients.blockedClientsList)
            
def clientUnblock(clientAddress):
    print("clientUnblock called")
    for clients in activeClientsList:
        if(clients.clientAddress == clientAddress):
            blockedIpIndexStart = decodedMessage.find("[") + 1
            blockedIpIndexEnd = decodedMessage.find("]", blockedIpIndexStart)
            blockedPortIndexStart = decodedMessage.find("[",blockedIpIndexEnd) + 1
            blockedPortIndexEnd = decodedMessage.find("]",blockedPortIndexStart)
            blockedIpAddress = decodedMessage[blockedIpIndexStart:blockedIpIndexEnd]
            blockedPortAddress = decodedMessage[blockedPortIndexStart:blockedPortIndexEnd]
            blockedPortAddress = int(blockedPortAddress)
            blockedClientAddress = (blockedIpAddress, blockedPortAddress)
            clients.blockedClientsList.remove(blockedClientAddress)
            print(clients.blockedClientsList)
    
print("The server is ready to receive.")
while True:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message, clientAddress = serverSocket.recvfrom(2048)
    decodedMessage = message.decode()
    
#   Add a new client to the activeClientsList
    if (decodedMessage.lower() == "!join"):
        print(time)
        clientJoin()
        print("Active users: ")
        for clients in activeClientsList:
            print("{", end="")
            print(clients.clientAddress, end=", ")
            print(clients.userName, end=", ")
            print(clients.muteStatus, end=", ")
            print(clients.blockedClientsList, end="}")
            print()
        print()
        
#   remove client from the activeClientsListBased on their clientAddress   
    elif (decodedMessage.lower() == "!quit"):
        print(time)
        clientQuit(clientAddress)
        if(len(activeClientsList)>0):
            print("Active users: ")
            for clients in activeClientsList:
                print("{", end="")
                print(clients.clientAddress, end=", ")
                print(clients.userName, end=", ")
                print(clients.muteStatus, end=", ")
                print(clients.blockedClientsList, end="}")
                print()
                print()
        else:
            print("No active users")
            print()
        
#     mute chat room
    elif (decodedMessage.lower() == "!mute"):
        print(time)
        clientMute(clientAddress)
        print("Active users: ")
        for clients in activeClientsList:
            print("{", end="")
            print(clients.clientAddress, end=", ")
            print(clients.userName, end=", ")
            print(clients.muteStatus, end=", ")
            print(clients.blockedClientsList, end="}")
            print()
        print()
        
#     unmute chat room
    elif (decodedMessage.lower() == "!unmute"):
        print(time)
        clientUnmute(clientAddress)
        print("Active users: ")
        for clients in activeClientsList:
            print("{", end="")
            print(clients.clientAddress, end=", ")
            print(clients.userName, end=", ")
            print(clients.muteStatus, end=", ")
            print(clients.blockedClientsList, end="}")
            print()
        print()
    
#     block a specific user by their client address use !block [ipaddress][portnumber] format
    elif (decodedMessage.lower().find("!block") == 0):
        print(time)
        clientBlock(clientAddress)
        print("Active users: ")
        for clients in activeClientsList:
            print("{", end="")
            print(clients.clientAddress, end=", ")
            print(clients.userName, end=", ")
            print(clients.muteStatus, end=", ")
            print(clients.blockedClientsList, end="}")
            print()
        print()
            
#     unblock a specific user by their client address use !unblock [ipaddress][portnumber] format
    elif (decodedMessage.lower().find("!unblock") == 0):
        print(time)
        clientUnblock(clientAddress)
        print("Active users: ")
        for clients in activeClientsList:
            print("{", end="")
            print(clients.clientAddress, end=", ")
            print(clients.userName, end=", ")
            print(clients.muteStatus, end=", ")
            print(clients.blockedClientsList, end="}")
            print()
        print()
#   if message is tno 
    else:
        print(time)
        clientSend(clientAddress)
        print("Active users: ")
        for clients in activeClientsList:
            print("{", end="")
            print(clients.clientAddress, end=", ")
            print(clients.userName, end=", ")
            print(clients.muteStatus, end=", ")
            print(clients.blockedClientsList, end="}")
            print()
        print()
