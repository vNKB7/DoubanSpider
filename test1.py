import urllib.request

url = "https://movie.douban.com/subject/26662193/comments?status=P"
data = urllib.request.urlopen(url).read()
data = data.decode('UTF-8')
print(data)