import os, sys

input_dir = sys.argv[1]

# CMD find > git_files.txt

os.system('find "{}" -name .git > git_files.txt'.format(input_dir))
pwd = os.environ['PWD']
# open git_files.txt

git_out = ''

f = open('git_files.txt','r')
git_files = f.readlines()
f.close()
if len(git_files) > 0 and len(git_files[0]) > len('\n'):
     for git in git_files:
        path = git.replace('.git','')
        git_out += 'Repo:' + path.split('/')[-2] + '\n'
        git_out += '{\n    '
        os.chdir(path.replace('\n',''))
        os.system('git status > {}/git_out.txt'.format(pwd))
        g = open('{}/git_out.txt'.format(pwd), 'r')
        status = g.readlines()
        g.close()
        git_out += '    '.join(status) + '\n}\n'

os.chdir(pwd)
h = open('git_out.json','w')
h.write(git_out)
h.close()

os.system('rm git_out.txt')
os.system('rm git_files.txt')


        