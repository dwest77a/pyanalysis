path_to_test_dir = 'scdiff'

file1 = 'local.txt'
file2 = 'playbook.txt'

f = open(path_to_test_dir + '/' + file1)
file1con = f.readlines()
f.close()

f = open(path_to_test_dir + '/' + file2)
file2con = f.readlines()
f.close()

lines = {}

f1lines = len(file1con)
shared_lines = 0
f2lines = 0

for x in range(len(file1con)):
    line = file1con[x].replace('\n','')
    line = line.replace(' ','')
    if not (line == '' or line.startswith('#')):
        lines[line] = 1
    
for y in range(len(file2con)):
    line = file2con[y].replace('\n','')
    line = line.replace(' ','')
    if not (line == '' or line.startswith('#')):
        if line in lines:
            lines[line] = 0
            shared_lines += 1
            f1lines -= 1
        else:
            lines[line] = 2
            f2lines += 1

f2l, f1l, shared = '','',''

for line in lines.keys():
    if lines[line] == 2:
        f2l += line + '\n'
    elif lines[line] == 1:
        f1l += line + '\n'
    else:
        shared += line + '\n'

print('Shared: ',shared_lines)
f = open(path_to_test_dir + '/shared','w')
f.write(shared)
f.close()
print('local-only:', f1lines)
f = open(path_to_test_dir + '/local-only','w')
f.write(f1l)
f.close()
print('playbook-only:',f2lines)
f = open(path_to_test_dir + '/playbook-only','w')
f.write(f2l)
f.close()
