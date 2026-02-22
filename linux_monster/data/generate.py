import os
import sys
import time
import random
import subprocess

red = '\033[1;31m'
blue = '\033[1;36m'
purple = '\033[2;35m'
yellow = '\033[1;33m'
green = '\033[1;32m'
plain = '\033[1;0m'

class generate:
  def __init__(self,*args):
    self.keywords = list(args)
    
  def process_data(self):
    data_str = list()
    data_int = None
    for data in self.keywords:
      if isinstance(data, str):
        if ':' in data:
          parts = data.split(':')
          if len(parts) == 3:
            try:
              day, month, year, full_year = (parts[0]), (parts[1]), (parts[2][-2:]), parts[2]
              data_int = [day,month,year,full_year]
            except ValueError:
              sys.stderr.write(f'Error parsing {parts}')
          pass
        else:    
          data_str.append(data)
    
    return data_str, data_int 
  
  def password_total(self):
    total = 0
    str_data, int_data = self.process_data()
    for each in str_data:
      total += len(each)
    
    return total * 21
  
  def write_password(self):
    str_data,int_data = self.process_data()
    special_chars = ['@','&','!','#','*','.','$']
  
    data = random.choice(str_data)
    if isinstance(data, str):
      init_chars = ''.join(random.choice([char.upper(), char.lower()]) for char in data)
      spec_chars = random.choice(special_chars)
      if int_data != None:
        birth_data = random.choice(list(int_data))
        format_ = [
          f'{init_chars}{spec_chars}',
          f'{init_chars}{birth_data}',
          f'{spec_chars}{init_chars}{birth_data}',
          f'{init_chars}{spec_chars}{birth_data}'
          ]
      else:
        format_ =[
          f'{init_chars}{spec_chars}',
          f'{spec_chars}{init_chars}'
          ]
        
    
    return random.choice(format_)

  
banner = f'''
{blue}
Take keywords, return a password
  .       .
,-| . ,-. |- . ,-. ,-. ,-. ,-. . .            
| | | |   |  | | | | | ,-| |   | |     
`-^ ' `-' `' ' `-' ' ' `-^ '   `-|    
                                /|                     
                               `-'
Entering a full date of birth should
be in this format >>> Day:Month:Year

{yellow}
Note :
You can enter help | exit when necessary
{plain}
'''    
os.system('cls' if os.name == 'nt' else 'clear')
def take_keywords():
  print(banner)
  keywords_collected = set()
  i = 0
  while i >= 0:
    value = input("Keyword >>> ").lower()
    value = value.strip()
    if value != "" and value != 'help' and value != 'exit':
      keywords_collected.add(value)
      i += 1
    elif value == 'help':
      subprocess.run(['xdg-open','https://github.com/harkerbyte'])
    elif value == 'exit':
      break
    else:
      if not len(keywords_collected) <= 0:
        file = input(f'\n{purple}Name the dictionary : {plain}').strip()
        if '.' in file:
          file,ext = file.split('.')
        
        file = f'{file}.txt'
        
        if not os.path.exists(f'password/{file}'):
          collect_passwords = set()
          generator = generate(*keywords_collected)
          total_returnee = generator.password_total()
          while len(collect_passwords) < total_returnee:
            f_password = generator.write_password()
            print(f'{yellow}Retrieved {f_password}{plain}')
            collect_passwords.add(f_password)
            i += 1
          
          parse_dict = list(collect_passwords)
          save_to = open(f'password/{file}', 'a')
          for data in parse_dict:
            save_to.write(f'{data}\n')
          
          print(f'{green}Dictionary saved >>> password/{file}{plain}')
          break
        
        sys.stderr.write(f'{red}{file} already exists{plain}')
        break
        
if __name__ == '__main__':
  take_keywords()