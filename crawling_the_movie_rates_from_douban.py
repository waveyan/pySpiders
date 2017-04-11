from urllib import request
import requests
from bs4 import BeautifulSoup
import re
import csv

headers={
	"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

def getUser():
	user={}
	for i in range(10):
		req=request.Request("https://movie.douban.com/subject/25765735/reviews?start="+str(i*20),headers=headers)
		bsObj=BeautifulSoup(request.urlopen(req))
		for x in bsObj.findAll('a',{"class":"author"}):
			user[x.find().get_text()]=x.attrs['href']
	return user

def getUser_Movied_rating(users):
	#进入用户主页
	people=0
	for user in users:
		people+=1
		print("第"+str(people)+"个")
		user_movie_rating=[]
		session=requests.Session()
		req=session.get(users[user],headers=headers)
		print("User Cookie: ")
		print(req.cookies.get_dict())
		bsObj=BeautifulSoup(req.text)
		for x in bsObj.findAll("div",{"id":"movie"}):
			#获得看过电影页面
			looked_url=x.findAll('a')[1].attrs['href']
			#获取电影评分
			for i in range(10):
				req=request.Request(looked_url+"?start="+str(i*15)+"&amp;sort=time&amp;rating=all&amp;filter=all&amp;mode=grid",headers=headers)
				looked_bsObj=BeautifulSoup(request.urlopen(req))
				for y in looked_bsObj.findAll("div",{"class":"grid-view"}):
					for z in y.findAll("div",{"class":"info"}):	
						movie=z.find("em").get_text().split(' ')[0]
						#有些电影没有评分,评分在<span class="date">上一个span标签里
						rating=z.find("span",{"class":re.compile("rating\d{1}\-t")})
						#['ratingX-t']
						if(rating):
							rating=rating.attrs["class"][0][6]
							user_movie_rating.append((user,movie,rating))
		logCsv(user_movie_rating)



def logCsv(user_tuple):
	with open("movie_rating.csv","a+") as f:
		writer=csv.writer(f)
		for x in user_tuple:
			writer.writerow(x)

getUser_Movied_rating(getUser())