import os

def difference(path, file1, file2, write=False):

    path_to_test_dir = path

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
    if write:
        f = open(path_to_test_dir + '/shared','w')
        f.write(shared)
        f.close()
    print('file1: only', f1lines)
        f = open(path_to_test_dir + '/f1only','w')
        f.write(f1l)
        f.close()
    print('file2 only:',f2lines)
        f = open(path_to_test_dir + '/f2only','w')
        f.write(f2l)
        f.close()

if __name__ == "__main__":
    # Expect `python scdiff.py /path/ file1 file2 y`
    path  = sys.argv[1]
    file1 = sys.argv[2]
    file2 = sys.argv[3]
    write = (sys.argv[4]=='y')

    difference(path, file1, file2, write=write)