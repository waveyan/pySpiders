from urllib.request import urlopen,urlretrieve,Request
from bs4 import BeautifulSoup
headers={'User-Agent':'Mozilla/5.0 (iPhone;U; CPU iPhone OS 3_0 like Mac OS X;en-us) AppleWebKit/528.18 (KHTML,like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'}
def download(url,title):
# url='http://www.11wa.com/show/21336.html'
	req=Request(url,headers=headers)
	bs=BeautifulSoup(urlopen(req))
	bs=bs.find('div',{'class':'show_player_gogo'})
	links=bs.findAll('a')
	i=0
	for x in links:
		if not x.get_text()=='高清中字':
			break;
		elif title.find('血战钢锯岭')!=-1:
			# i+=1
			href=x.attrs['href']
			req=Request(href,headers=headers)
			bs=BeautifulSoup(urlopen(req))
			href=bs.find('iframe').attrs['src']
			req=Request(href,headers=headers)
			bs=BeautifulSoup(urlopen(req))
			src=bs.find('video').attrs['src']
			# print(bs.a.attrs['href'])
			# print(title+str(i)+' downloading...')
			urlretrieve(src,title+'.mp4')
			print(title+' downloaded')

# baseUrl=r'http://www.11wa.com/type/5.html'
baseUrl=r'http://www.11wa.com/type/1/1.html'
def complicated(baseUrl):
	req=Request(baseUrl,headers=headers)
	bs=BeautifulSoup(urlopen(req))
	nextUrl=bs.find('div',{'class':'pages'}).findAll('a')[-1]
	baseUrl='http://www.11wa.com'+nextUrl.attrs['href']
	bs=bs.find('div',{'class':'index-area clearfix'})
	for x in bs.findAll('a'):
		# print(x.attrs['href'])
		try:
			download(x.attrs['href'],x.attrs['title'])
		except Exception as e:
			print('出错了：',e)
	complicated(baseUrl)

complicated(baseUrl)


