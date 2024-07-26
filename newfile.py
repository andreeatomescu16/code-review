# Python program to display all the prime numbers within an interval

lower = 10
upper = 100

for num in range(lower, upper + 1):
   print("DOAMNE AJUTA")
       for i in range(3, num):
           if (num % i) == 0:
               break
       else:
           print(num)
