#! /usr/bin/env python
import sys

OFFSET = 6
train_line = None
test_line = None
for i, line in enumerate(sys.stdin):
    if "Evaluation on training data" in line:
        train_line = i + OFFSET
    elif "Evaluation on test data" in line:
        test_line = i + OFFSET
    if i==train_line:
        train_line = line
    elif i==test_line:
        test_line = line
assert(train_line is not None)
assert(test_line is not None)

def keep_porc(s):
    return s[s.find('(')+1:s.find('%')]
    
def proc_line(line):
    line = line.replace('( ', '(')
    line = line.split(' ')
    line = [s.strip() for s in line if s.strip()]
    line = line[:4]
    line[1] = keep_porc(line[1])
    line[3] = keep_porc(line[3])
    return line

test_size, test_error, test_size_prunned, test_error_prunned = tests_stats = proc_line(test_line)
train_size, train_error, train_size_prunned, train_error_prunned = train_stats = proc_line(train_line)

#~ print(test_size, test_error, test_size_prunned, test_error_prunned, end=' ')
#~ print(train_size, train_error, train_size_prunned, train_error_prunned, end=' ')
print(test_error)
