# Python program to display all the prime numbers within an interval

lower = 10
upper = 100

for num in range(lower, upper + 1):
   # all prime numbers are greater than 1
   print("DOAMNE AJUTA")
   if num > 1:
       for i in range(2, num):
           if (num % i) == 0:
               break
       else:
           print(num)
