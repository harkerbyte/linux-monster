import os
import sys
import requests
import time
import base64
from datetime import timedelta
import concurrent.futures as CF
from linux_monster.main import red,yellow,green,blue,plain,base_dir


def refactor(protocol, value, list_, auth_re, save):
  os.system('cls' if os.name == 'nt' else 'clear')     
  protocol.strip()
  value.strip()
  try:
    if protocol == "https" and auth_re:
      if value == "2":
        #username:password:address:port
        user,pass_,address,port = list_.split(':')
        if all((user,pass_,address,port)):
          if save:
            return f'{user}:{pass_}:{address}:{port}:{protocol}'
          else:
            return {f'{protocol}' : f'{protocol}://{user}:{pass_}@{address}:{port}'}
        
      elif value == "3":
        #address:port:username:password
        address,port,user,pass_ = list_.split(':')
        if all((address,port,user,pass_)):
          if save:
            return f'{user}:{pass_}:{address}:{port}:{protocol}'
          else:
            return {f'{protocol}' : f'{protocol}://{user}:{pass_}@{address}:{port}'}
          
    else:
      if value == "1":
        address,port = list_.split(':')
        if all((address,port)):
          if save:
            return f'{address}:{port}:{protocol}'
          else:
            return {f'{protocol}' : f'{protocol}://{address}:{port}'}
  except ValueError:
    return None

def migrator():
  banner = f"""
  .-..-. _                    .-.
  : `' ::_;                  .' `.
  : .. :.-. .--. .--.  .--.  `. .' .--.
  : :; :: :' .; :: ..'' .; ;  : : ' '_.'
  :_;:_;:_;`._. ;:_;  `.__,_; :_; `.__.'
          .-. :
          `._.'
  SUPPORTED FORMATS            
  [1] address:port
  [2] username:password:address:port
  [3] address:port:username:password
  [4] exit
  """
  print(banner)

  value = str(input('Format : ').strip())
  if value == '4' or value == 'exit':
    sys.exit()
  protocol = str(input('Protocol : ').lower())
  auth_re = False
  if protocol == "https":
    auth_ = input('Requires authentication [Yes | No]: ').lower()
    if auth_ != "no":
      auth_re = True
    
  
  file_name = input('Migrating file [file_name.txt] : ')


  if protocol == 'https':
    c_http = input('Register http protocols [Yes | No] : ').lower()

  mv_to_path = f'{base_dir}/data/proxy.txt'
  os.makedirs(os.path.dirname(mv_to_path), exist_ok = True)

  with open(mv_to_path, 'w') as existing_proxy:
    pass


  if os.path.exists(file_name):
    name, ext = os.path.splitext(file_name)
    if ext != '.txt':
      print(f'{red}Provide a valid .txt document{plain}')
      sys.exit()
  
    with open(file_name, 'r') as proxy_file:
      proxies = [line.strip() for line in proxy_file.readlines() if line.strip()]
  
    uni_url = 'https://facebook.com'
    def migrate_proxy(proxy):
      with open(mv_to_path, 'w') as migrating:
        try:
          start_time = time.time() 
          if value == "2" or value == "3":
            pro_us_pa_add_po = refactor(protocol, value, proxy, True, False)
          
            grabber = pro_us_pa_add_po[f'{protocol}']
            us_pa = grabber.split('@')[0].split('//')[1]
            auth_encode = base64.b64encode(us_pa.encode()).decode()
            host_url = grabber.split('@')[1]
            headers = {
              'Proxy-Authorization' : f'Basic {auth_encode}'
            }
            proxies = {
              'https' : f'{host_url}',
              'http' : f'{host_url}'
            }
            requests.get(uni_url, headers = headers, proxies = proxies, timeout = 10)
          else:
            requests.get(uni_url, proxies = refactor(protocol, value, proxy, True if auth_re else False, False), timeout = 10)
          
          saver = refactor(protocol, value, proxy, True if auth_re else False, True)
          migrating.write(f'{saver}\n')
          time_taken = str(timedelta(seconds = time.time() - start_time ))  
          print(f'{green}Protocol - {protocol} : Loadtime {time_taken} - Saved{plain}')
        
        except requests.exceptions.SSLError:
          time_taken = str(timedelta(seconds = time.time() - start_time ))
          if c_http == 'yes':
            migrating.write(f'{proxy}:http\n')
            print(f'{yellow}Protocol - http : Loadtime {time_taken} - Saved{plain}')
       
        
        except (requests.exceptions.ConnectionError, requests.exceptions.ProxyError):
          print(f'{yellow}Proxy error : {proxy}{plain}')
        except OSError as os_err:
          print(f'{red} {os_err} {plain}')
      
        except Exception as error:
          if 'Read timed out' in error:
            print(f'{red}Connection blocked / Slow internet{plain}')
          if 'Connection broken' in error:
            print(f'{red}Connection interrupted{plain}')
          if 'check proxy URL' in error:
            print(f'{red}You\'ve choosen the wrong format.')
          else:
            print(red+error+plain)
  
    min_thread = min(100, len(proxies))
    with CF.ThreadPoolExecutor(max_workers = min_thread) as execute:
      execute.map(migrate_proxy, proxies)
      execute.shutdown(wait = True)
      with open(f'{base_dir}/data/proxy.txt', 'r') as registry:
        if len(registry.readline()) == 0:
          print(f'{red}Confirm that you have choosen the correct format, then try again{plain}')
        else:
          print('\nOperation complete')
    

if __name__ == "__main__":
  migrator()