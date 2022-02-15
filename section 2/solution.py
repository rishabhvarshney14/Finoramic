#  build a tool to automatically download python packages. 
import subprocess
import sys
import threading
import os

# Since the input given in dependencies.txt is not really a json data we have to manually iterate over the data
# and extract all the files that are needed
# getDependencies takes data as a string and returns a Dictionary object with module name as its key and its version as value
def getDependencies(data):
  dependencies = {}
  k = len('Dependencies')

  for i in range(len(data) - k):
    if data[i:i+k] == 'Dependencies':
      start = i+k 
      end = i+k 

      while end < len(data) and data[end] != '}':
        if data[start] != '{':
          start += 1
        end += 1
      
      for item in data[start+1:end].split(','):
        if item.strip():
          key, value = map(lambda x: x.strip(), item.split('=='))
          dependencies[key] = value 
      break 
  
  return dependencies

# Function to install a single package
# Installing of a package can failed because of build errors or OS Permission issues
def installPackage(package, version, failed=[]):
  # print('installing: ', package)
  try:
    subprocess.check_call(
      [sys.executable, "-m", "pip", "install", f"{package}=={version}", "--user"], 
      # Comment below attributes to see pacakge installing output
      stdout=subprocess.DEVNULL,
      stderr=subprocess.STDOUT
    )
  except:
    failed.append(package)

# function to install all the dependencies
def installDependencies(dependencies, threads=4):
  failed = []
  packages = list(dependencies.keys())

  for i in range(0, len(packages), threads):
    totalRunning = []
    for package in packages[i:i+threads]:
      temp = threading.Thread(target=installPackage, args=(package, dependencies[package], failed,))
      temp.start()
      totalRunning.append(temp)
    
    for thread in totalRunning:
      thread.join()
  
  if not failed:
    print("success")
  else:
    print("Following packages failed to install:")
    print('\n'.join(failed))

# Main function to read and install dependencies
# Take two params filename (path to the dependencies file) and threads (how many multiple package should install at a time)
def main(filename, threads=4):
  if not os.path.exists(filename):
    print(filename, "does not exist!")
    return

  with open("dependencies.txt", encoding='utf-8', mode='r') as data:
    data = data.read().strip()
    dependencies = getDependencies(data)
    installDependencies(dependencies, threads=threads)

if __name__ == "__main__":
  main('dependencies.txt', threads=8)