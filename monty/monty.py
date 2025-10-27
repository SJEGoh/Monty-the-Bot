from random import randint

opendoor = [False, False, False]
reward = [False, False, False]

reward[randint(0, 2)] = True


choice = int(input("Choose gate to open: ")) - 1
opendoor[choice] = True


wrong = []
for i in range(0, 3):
    if opendoor[i] == False and reward[i] == False:
        wrong.append(i + 1)
    
if len(wrong) == 2:
    reveal = wrong[randint(0, 1)]
    print(f"Gate {reveal} has no reward\n")
    opendoor[reveal - 1] = True
else:
    print(f"Gate {wrong[0]} has no reward\n")
    opendoor[wrong[0] - 1] = True 

ss = input("Stay or Switch? ")

if ss == "Stay":
    if reward[choice] == True:
        print("You won!")
    else:
        print("You lose")
elif ss == "Switch":
    for i in range(0, 3):
        if opendoor[i] == False:
            newchoice = i
        else:
            continue
    
    if reward[newchoice] == True:
        print("You won!")
    else:
        print("You lose")
