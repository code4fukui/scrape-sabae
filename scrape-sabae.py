import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os.path

def getHTML(url):
	if exists(url):
		return
	if not (url.endswith(".html") or url.endswith(".htm") or url.endswith("/")):
		return
	print("----")
	print("URL: " + url)
	try:
		f = urlopen(url)
		content = f.read()
		
		s = content[:1024].decode("ascii", errors="replace")
		
		enctype = "utf-8"
		match = re.search(r"char=['\']?([\w-]+)", s)
		if match:
			enctype = match.group(1)
		else:
			match = re.search(r"charset=['\']?([\w-]+)", s)
			if match:
				enctype = match.group(1)
		print(enctype)
		
		data = content.decode(enctype)
		save(url, data)
	#	print(data)
		
		soup = BeautifulSoup(data, "html.parser")
		tags = soup.find_all("a")
		
		for tag in tags:
			url2 = tag.get("href")
			url3 = urljoin(base, url2)
			n = url3.find("#")
			if n >= 0:
				url3 = url3[:n]
			print(url3)
			if url3.startswith(base):
				getHTML(url3)
	except:
		f = open('404.txt','a')
		f.write(url + '\n')
		f.close()

def save(url, data):
	fn = ren(url)
	with open("cache/" + fn, mode = 'w', encoding = 'utf-8') as fw:
		fw.write(data)

def exists(url):
	fn = ren(url)
	return os.path.exists("cache/" + fn)

def ren(url):
	url = re.sub("/", "_", url)
	url = re.sub(":", "_", url)
	url = re.sub("\?", "_", url)
	url = re.sub(" ", "_", url)
	url = re.sub("\n", "_", url)
	url = re.sub("\r", "_", url)
	url = re.sub("\t", "_", url)
	return url

base = "https://www.city.sabae.fukui.jp/"

getHTML(base)
