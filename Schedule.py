count = 0
yep = "yes"
list = []
data_list = []

class data:
    def __init__ (self, activity, id, counter):
        self.activity = activity
        self.id = id
        self.counter = counter

    def __str__(self):
        return self.activity
        #self.count = count

while yep == "yes":
    count = count +1
    data1 = data(input("activity: "), int(input("id: ")), counter=count)
    print(data1.counter)
    data_list.append(data1)
    list.append(data1.id)

    yep = input("continue: ")

newlist = sorted(data_list, key=lambda x: x.id, reverse=False)
#print(newlist)
for x in newlist:
    print(x)

#yep = a button input (submit button)
#class data = model table
