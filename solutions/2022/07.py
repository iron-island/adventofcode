import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def get_curr_dict(hierarchy, dirs):
  curr_dict = dirs
  for h in hierarchy:
    curr_dict = curr_dict[h]

  return curr_dict

def populate_curr_dict(hierarchy, dirs, file_ls):
  curr_dict = get_curr_dict(hierarchy, dirs)

  #if not (curr_dict.get(file_ls[1])):
  if (file_ls[1] not in curr_dict.keys()):
    curr_dict[file_ls[1]] = {}

    if ("dir" not in file_ls[0]):
     curr_dict[file_ls[1]]["size"] = file_ls[0]
  else:
    #curr_dict[file_ls[1] + "_v2"] = {}

    #if ("dir" not in file_ls[0]):
    # curr_dict[file_ls[1] + "_v2"]["size"] = file_ls[0]
    print(f'ERROR in populate_curr_dict: {file_ls[1]} already in curr_dict:')
    print(f'{curr_dict}')
    breakpoint()

  return curr_dict

def compute_sizes(dirs, dir_dict, dir_dict2, total_size, dir_sizes):
  size = 0

  for key, contents in dirs.items():
    #print(f'Computing file/dir {key} with contents {contents}')
    if (contents.get('size')):
      size = size + int(contents['size'])
    else:
      dir_size, total_size  = compute_sizes(contents, dir_dict, dir_dict2, total_size, dir_sizes)
      dir_sizes.append(dir_size)
      #dir_dict[key] = dir_size

      if (dir_size <= 100000):
        total_size = total_size + dir_size

      size = size + dir_size

    #if (size < min_dir_size) and (size > 8381165):
    #  min_dir_size = size


  return int(size), total_size

# initialize variables
input_file = "../../inputs/2022/input07.txt"
#input_file = "example07.txt"

dirs = {}
curr_dir = {}
hierarchy = []
curr_dict = dirs

total_size = 0
dir_dict = {"/": 0}
dir_dict2 = {"/": 0}

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()

    # process
    skip_next_read = 0
    #print(txtfile_line)
    if ("$" in txtfile_line):
      if ("cd " in txtfile_line):
        directory = txtfile_line.split(" ")

        if (".." not in txtfile_line):
          curr_dir = directory[2]
          #if not curr_dict.get(curr_dir):
          if curr_dir not in curr_dict.keys():
            curr_dict[curr_dir] = {}
          
          # add to hierarchy
          hierarchy.append(curr_dir)
        elif (".." in txtfile_line):
          hierarchy.pop()

        # traverse directory tree
        curr_dict = get_curr_dict(hierarchy, dirs)

      elif ("ls" in txtfile_line):
        # read files
        txtfile_line = txtfile.readline()
        txtfile_line = txtfile_line.strip()
        while ("$" not in txtfile_line):
          file_ls = txtfile_line.split(" ")
     
          # add file list to dictionary     
          #print(f'adding to list: {curr_dict})')

          # add directory to dir_dict
          if (file_ls[0] == "dir"):
            #if (file_ls[1] in dir_dict.keys()):
            #  file_ls[1] = file_ls[1] + "_v2"

            dir_dict[file_ls[1]] = 0
            dir_dict2[file_ls[1]] = 0

          curr_dict = populate_curr_dict(hierarchy, dirs, file_ls)

          txtfile_line = txtfile.readline()
          txtfile_line = txtfile_line.strip()
          if len(txtfile_line) == 0:
            break

        skip_next_read = 1

    # read next line
    if not skip_next_read:
      txtfile_line = txtfile.readline() 

# compute directory sizes
#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint(dirs)
total_size = 0
dir_sizes = []
root_size, total_size = compute_sizes(dirs, dir_dict, dir_dict2, total_size, dir_sizes)
#pretty_print.pprint(dir_dict)

# compute total
min_dir_size = 70000000
required_size = 30000000 - (min_dir_size - root_size)
for d in dir_sizes:
  if (d < min_dir_size) and (d >= required_size):
    min_dir_size = d

# queue
#myqueue = []
#myqueue.append('a')
#myqueue.append('b')
#myqueue.append('c')
#myqueue # ['a', 'b', 'c']
#myqueue.pop(0) # ['b', 'c']
#myqueue.index('c') # 1
#myqueue.pop(1) # ['b']


# print answer
ans1 = total_size
ans2 = min_dir_size
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
