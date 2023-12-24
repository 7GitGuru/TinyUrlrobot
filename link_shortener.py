import pyshorteners

URL = input("Enter the URL: ")

reduce = pyshorteners.Shortener()
output_URL = reduce.tinyurl.short(URL)

print("The shorten URL is: " + output_URL)