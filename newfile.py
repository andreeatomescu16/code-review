# Python program to display all the prime numbers within an interval

lower = 10
upper = 100

for num in range(lower, upper ):
       for i in range(2, num):
           if (num % i) == 0:
               break
       else:
           print(num)
