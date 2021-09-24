import requests
import json
import time
import re

def find_beatmap_number(file): #곡 파일에서 곡 번호를 알아내기
	aaa = open(file,mode="r",encoding="utf-8")
	bbb = aaa.readlines()
	numberstr = ''
	numberlist2 = []
	p = re.compile("mania[/][0-9]{3,10}")
	for i in bbb:
		numberstr = numberstr + i
	numberlist = p.findall(numberstr)
	for i in numberlist:
		numberlist2.append(int(i[6:]))
	return numberlist2

userfile = open("userlist.txt",mode="r",encoding="utf-8")
usertemp = userfile.readlines()
fff = []
for i in usertemp:
	prog = re.search("users[/][0-9]{3,10}",i)
	a = prog.group(0)
	fff.append(a[6:])


beatmaplist = find_beatmap_number("songlist.txt")

output = []

def getscore(username):
	errorcount = 0
	try:	
		url = "https://osu.ppy.sh/users/"+str(username)+"/scores/recent?mode=mania&limit=100"
		html = requests.get(url)
		if html == '<Response [429]>':
			raise Exception('429 error')
		print(html)
		ob1 = html.json()
			
		for replay in ob1:
			exsisting = False
			id = int(replay['beatmap']['id'])
			if id not in beatmaplist:
				continue
			if len(output) != 0:
				for i in output:
					if id == int(i['id']):
						exsisting = True
						break
			if exsisting == False:
				a = {}
				a['id'] = id
				a['title'] = replay['beatmapset']['title']+" "+replay["beatmap"]["version"]
				a['stars'] = replay['beatmap']['difficulty_rating']
				a['imageurl'] = replay['beatmapset']['covers']['list@2x'].replace("\\","")
				a['score'] = []
				output.append(a)
			exsisting = False
			for i in output:
				if id == i['id']:
					for k in i['score']:
						if replay['id'] == k['id']:
							exsisting = True
							break
			if exsisting == False:
				for i in output:
					if id == i['id']:
						score = {}
						score['id'] = replay['id']
						score['userid'] = username
						score['username'] = replay['user']['username']
						score['score'] = replay['score']
						score['accuracy'] = replay['accuracy']
						count = {}
						count['320'] = replay["statistics"]["count_geki"]
						count['300'] = replay["statistics"]["count_300"]
						count['200'] = replay["statistics"]["count_katu"]
						count['100'] = replay["statistics"]["count_100"]
						count['50'] = replay["statistics"]["count_50"]
						count['miss'] = replay["statistics"]["count_miss"]
						score['counts'] = count
						i['score'].append(score)
						break
	except Exception as e:
		print(e)
		time.sleep(3)
		errorcount +=1
	finally:
		time.sleep(0.5)

for i in fff:
	getscore(i)

jsonstr = json.dumps(output)
a = open("weekly.json",mode='w',encoding='utf-8')
a.write(jsonstr)
