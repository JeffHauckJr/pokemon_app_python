number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def check_for_ten():
    for x in number:
        if x <= 9:
          print("This is not enough " + str(x))
        else:
          print("This is " + str(x)) 
         
check_for_ten()
