import glob
stegos = {}
filenames = glob.glob('extracted_messages\\*.txt')
for filename in filenames:
    try:
        with open(filename,'r') as f:
            content = f.read()
            print(content)
    except:
        pass
input()
