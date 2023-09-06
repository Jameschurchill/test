print("Give me two numbers, and I'll divide them.")
print("Enter 'q' to quit.")
while True:
 first_number = input("First number: ")
 if first_number == 'q':
     break
 second_number = input("Second number: ")
 if second_number == 'q':
     break
 try:
   answer = float(first_number) / float(second_number)
 except ZeroDivisionError:
   print("You can't divide by 0!")
 except ValueError:
   print("input error")
 else:
   print(answer)