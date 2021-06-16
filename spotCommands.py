

def main():
    print("Spot command.\n")

    while(True):
        command = str(input("Enter a command (commands must start with spot) or enter 'end' to stop commanding spot: "))
        print("\n")

        command = command.lower()

        if(command == "stop" or command == "estop"):
            spotEstop()
            break
        elif(command == "end"):
            spotShutdown()
            break
        elif "spot" not in command:
            print("Command does not begin with spot. Spot doesn't know you're talking to him.\n")
        else:
            selectCommand(command)



def spotEstop():
    print("Spot EMERGENCY stop\n")

def spotShutdown():
    print("Spot shutdown\n")

def selectCommand(command):
    command = command.replace("spot ", "")
    print("Command: " + command + "\n")
    if "forward" in command:
        spotForward()
    elif "backward" in command:
        spotBackward()
    elif "right" in command:
        spotRight()
    elif "left" in command:
        spotLeft()

def spotForward():
    print("Spot moving forward\n")

def spotBackward():
    print("Spot moving backward\n")

def spotRight():
    print("Spot turning left\n")

def spotLeft():
    print("Spot turning right\n")

main()