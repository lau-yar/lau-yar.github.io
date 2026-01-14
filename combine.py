import sys
import re
import os
import rjsmin

def combineContent(file, curDir, imported):
  if file in imported: return r'' # already imported
  imported.add(file)
  with open(curDir + '/' + file, 'r') as file:
    content = file.read()
  # import files
  pattern = r'(import +.*? +from +[\'"](.*?)[\'"]\s*)'
  matches = re.findall(pattern, content)
  for oldText, importFile in matches:
    fileContent = combineContent(importFile, curDir, imported)
    content = content.replace(oldText, fileContent + '\n\n')
  return content

def main():
  if len(sys.argv) < 2:
    print("Usage: python combine.py <the entry js file>")
  else:
    imported = set()
    content = combineContent(sys.argv[1], os.path.dirname(sys.argv[1]), imported)
    # get rid of export default 
    content = content.replace("export default ", '')
    # replace "*/*.wgsl" with "*/optimized_*.wgsl"
    # use it when you also obfuscated your shader code
    pattern = r'[\'"](.*.wgsl)[\'"]'
    matches = re.findall(pattern, content)
    for oldText in matches:
      content = content.replace(oldText, os.path.dirname(oldText) + "/optimized_" + os.path.basename(oldText))
    with open(os.path.splitext(os.path.basename(sys.argv[1]))[0] + "-full.js", 'w') as file:
      file.write(rjsmin.jsmin(content))
    
if __name__ == "__main__":
  main()