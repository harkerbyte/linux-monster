import os
import json

green = '\033[2;32m'
plain = '\033[2;0m'

base_dir = os.path.dirname(os.path.abspath(__file__)) 
def write_json(value):
  if not os.path.exists(value):
    init = open(value, 'w')
    init.write('{}')
    init.close()
    return ['completed']
  return True
    
class memory:
  def __init__(self,target,type_,last_checked,dict_path):
    self.target, self.type_ = target, type_
    self.last_checked, self.dict_path = last_checked, dict_path
      
  def which_path(self):
    google_mem = f'{base_dir}/google.json'
    facebook_mem = f'{base_dir}/facebook.json'
    if self.type_ == 1:
      if write_json(google_mem):
        file = open(google_mem, 'r').readlines()
        if len(file) != 0:
          return google_mem
       #incase google.json had been unknowingly emptied
        init_ = open(google_mem, 'w')
        init_.write('{}')
        init_.close()
        return google_mem
    else:
      if write_json(facebook_mem):
        file = open(facebook_mem, 'r').readlines()
        if len(file) != 0:
          return facebook_mem
        #incase facebook.json had been unknowingly emptied
        init_ = open(facebook_mem, 'w')
        init_.write('{}')
        init_.close()
        return facebook_mem
    
  def update_(self):
    path = self.which_path()
    
    with open(path, 'r') as memo:
      memory = json.load(memo)
      try:
        memory[self.target]["index"] = self.last_checked
        memory[self.target]["dictionary"] = self.dict_path
      except KeyError:
        frame = {
          "index" : f'{self.last_checked}',
          "dictionary" : f'{self.dict_path}'
        }
        memory.update({f'{self.target}':frame})
        
      with open(path, 'w') as save_memory:
        json.dump(memory,save_memory,indent =2)
        save_memory.close()
      
  def read_(self):
    path = self.which_path()
    with open(path, 'r') as memo:
      memory = json.load(memo)
      try:
        memory[self.target]
        prev_index = memory[self.target]["index"]
        prev_dict = memory[self.target]["dictionary"]
        if prev_dict == self.dict_path:
          print(f'Resuming from where we last stopped ✅')
          re = open(self.dict_path, 'r')
          index = [line.strip() for line in re.readlines() if line.strip()]
          try: 
            return index.index(prev_index)
          except ValueError:
            print('Failed to do so: file content doesn\'t match')
            return None
        return None
      except KeyError:
        return None
      
  def terminate_(self):
    path = self.which_path()
    with open(path, 'r') as memo:
      memory = json.load(memo)
      try:
        del memory[self.target]
        with open(path, 'w') as save_rem:
          json.dump(memory, save_rem, indent = 2)
          save_rem.close()
      except KeyError:
        pass
      

  