#  build a tool to automatically download python packages. 
import subprocess
import sys

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

# Function to install a singal package
# Installing of a package can failed because of build errors or OS Permission issues
def installPackage(package, version):
  subprocess.check_call(
    [sys.executable, "-m", "pip", "install", f"{package}=={version}", "--user"], 
    # Comment below attributes to see pacakge installing output
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT
  )

# function to install all the dependencies
def installDependencies(dependencies):
  failed = []
  for package, version in dependencies.items():
    try:
      installPackage(package, version)
    except:
      failed.append(package)
  
  if not failed:
    print("success")
  else:
    print("Following packages failed to install:")
    print('\n'.join(failed))

with open("dependencies.txt", encoding = 'utf-8') as data:
  data = data.read().strip()
  dependencies = getDependencies(data)
  installDependencies(dependencies)
