import base64
from flask import Flask, request
import requests
from linux_monster.main import onload_proxy
import logging 
import os

app = Flask(__name__)
@app.route("/", defaults = {"path" : ""})

@app.route("/<path:path>", methods = ["GET", "POST"])
def proxy(path):
  if not path.startswith('https://') and not path.startswith('http://'):
    path =  f'https://{path}'
  
  print(path)
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
  }
  proxy_now = onload_proxy()
  if '@' in proxy_now:
    #protocol://user:pass@address:port
    proxy_url = proxy_now.split('@')[1]
  
    auth_encode = base64.b64encode(proxy_now.split('@')[0].split('//')[1].encode()).decode()
  
    headers["Proxy-Authorization"] = f"Basic {auth_encode}"
  
  else:
    #protocol://address:port
    proxy_url = proxy_now.split('//')[1]
    
  try:
    if request.method == "POST":
      response = requests.post(path, proxies = {'https' : proxy_url, 'http' : proxy_url}, headers = headers, data = request.data)
      
    else:
      response = requests.get(path, proxies = {'https' : proxy_url, 'http' : proxy_url}, headers = headers, params = request.args)
    
    
    return response.content
      
  except Exception as error:
    onload_proxy(pop = proxy_now)
    return f"Error : {error}"
 
def start():
  app.run(host='127.0.0.1', port = 8000) 
  
if __name__ == "__main__":
  os.system('cls' if os.name == 'nt' else 'clear')
  start()