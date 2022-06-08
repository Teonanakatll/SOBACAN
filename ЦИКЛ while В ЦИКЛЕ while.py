from winsound import Beep


finish = []
finish.append([2, 5, "img", True])
finish.append([3, 7, "img", False])
finish.append([4, 5, "img", False])
finish.append([7, 2, "img", True])
finish.append([4, 7, "img", False])

boxes = []

for i in range(len(finish)):
    boxes.append(finish[i][0:3])
    #for j in range(len(finish[i]) - 1):
        #boxes[i].append(finish[i][j])

#boxes[0][0] = 3

for fin in finish:
    fin[3] = False

win = True
fin = 0
while (fin < len(finish) and win):
    box = 0
    #print(box)
    while (box < len(boxes)):
        if (finish[fin][0:2] == boxes[box][0:2]):
            finish[fin][3] = True
            box = len(boxes)
            #print(box)
        box += 1
        print(box)
    win = win and finish[fin][3]
    fin += 1

if (win):
    Beep(750, 10)
    Beep(1750, 10)
            
