import requests as r
from bs4 import BeautifulSoup
from sys import argv
from multiprocessing.dummy import Pool as ThreadPool

'''
openbugbounty.org programs' scope scraper
Use: python3 obb_scraper.py [threads]
Default threads: 10
'''

def extract(prog):
	test = r.get(prog).text
	prog_soup = BeautifulSoup(test, "html.parser")
	for link in prog_soup.find_all('td'):
		try:
			if "None" not in link.string:
				for res in list(filter(lambda a: a != '\xa0', link.string.splitlines())):
					print(res, flush=True)
		except TypeError:
			pass


if __name__ == '__main__':
	try:
		obb = "https://www.openbugbounty.org"
		programs = []
		c = 0
		threads = 10
		if argv[1:]:
			threads = int(argv[1])
		#print("We use {} Threads".format(threads))
		for page in range(48):
			c+=1
			#print("\n\nPage {}: done\n\n".format(c))
			page = r.get('https://www.openbugbounty.org/bugbounty-list/page/{}'.format(page)).text
			soup = BeautifulSoup(page, "html.parser")
			for link in soup.find_all('a'):
				try:	
					if "/bugbounty/" in link.get('href') and "create" not in link.get('href'):
						prog = obb + link.get('href')
						programs.append(prog)
				except TypeError:
					pass
			pool = ThreadPool(threads)
			results = pool.map(extract, programs)
			pool.close()
			pool.join()
			programs = []
	except KeyboardInterrupt:
		print("Exiting")
