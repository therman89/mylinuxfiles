import json

line =""
with open("sample.json", "r") as f:
	line = f.readline()
data = json.loads(line)
data["TBS1"]["humi"] = 777
with open("sample.json", "w") as f:
	json.dump(data,f)
	f.write("\n")
	print data
