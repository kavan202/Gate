from test import mark
url = input("Enter the URL of the GATE exam result page: ")
score = mark(url)
print(f"Your score is: {score}")