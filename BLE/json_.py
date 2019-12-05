import json

data = {"TBS1":
		{
		"temp":1,
		"humi":2
		},
	"TBS2":
		{
		"temp":3,
		"humi":4
		}
	}
with open("sample.json","a") as f:
	json.dump(data,f)
	f.write("\n")
