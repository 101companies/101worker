import sys
import json
import os

def validate_runner(module):
    attrs = ['applicable', 'main']
    
        

def load_runners(path):
    
    sys.path.append(path)
    
    files = os.listdir(path)
    files = filter(lambda f: f != '__init__.py', files)
    files = filter(lambda f: not f.endswith('.pyc'), files)
    files = map(lambda f: os.path.join(path, f), files)
    files = filter(os.path.isfile, files)
    
    files = map(os.path.basename, files)
    
    files = map(lambda f: os.path.splitext(f)[0], files)
    
    modules = map(__import__, files)
    
    return modules
    

def main(argv):
    config = os.path.join(os.path.dirname(sys.argv[0]), '..', 'configs', argv[1])
    
    with open(config) as f:
        modules = json.loads(f.read())
    
    #print modules
    
    runners = load_runners(os.path.join(os.path.dirname(sys.argv[0]), 'runners'))
    print runners
    
if __name__ == '__main__':
    main(sys.argv)
    



