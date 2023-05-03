#   
#
#
#
#
#
#
#



import os
import shutil
import re

def peek_n(f, n=1):
    pos = f.tell()
    result = f.read(n)
    f.seek(pos)
    return result

def peek_until(f, target_char):
    pos = f.tell()
    chars = []
    while True:
        c = f.read(1)
        if not c:
            break
        chars.append(c)
        if c == target_char:
            break
    f.seek(pos)
    return ''.join(chars)

input_folder = ""
backup_folder = ""
output_folder = ""

def process_input_folder(folder):
    global input_folder
    input_folder = folder

def process_backup_folder(folder):
    global backup_folder
    backup_folder = folder

def process_output_folder(folder):
    global output_folder
    output_folder = folder


# Define state constants
STATE_NORMAL = 0
STATE_IN_PARENS = 1
STATE_IN_BRACKETS = 2
STATE_IN_CURLY_BRACKETS = 3
STATE_IN_QUOTE = 4
STATE_IN_QUOTE_TAG = 5
STATE_IN_WAIT_TAG = 6
STATE_SINGLE_PUNCTUATION = 7
STATE_DOUBLE_PUNCTUATION = 8
STATE_COMMENT = 9
# STATE_MENU = 10

state_names = {
    STATE_NORMAL: "STATE_NORMAL",
    STATE_IN_PARENS: "STATE_IN_PARENS",
    STATE_IN_BRACKETS: "STATE_IN_BRACKETS",
    STATE_IN_CURLY_BRACKETS: "STATE_IN_CURLY_BRACKETS",
    STATE_IN_QUOTE: "STATE_IN_QUOTE",
    STATE_IN_QUOTE_TAG: "STATE_IN_QUOTE_TAG",
    STATE_IN_WAIT_TAG: "STATE_IN_WAIT_TAG",
    STATE_SINGLE_PUNCTUATION: "STATE_SINGLE_PUNCTUATION",
    STATE_DOUBLE_PUNCTUATION: "STATE_DOUBLE_PUNCTUATION",
    STATE_COMMENT: "STATE_COMMENT",
    # STATE_MENU: "STATE_MENU",
}

PUNCTUATION_SINGLE = [',', '-', ':']
PUNCTUATION_FULL = ['.', '?', '!']

prevstate = 0
WAIT_TAG_PATTERN = r"w=\d+\.\d+}"

# Iterate through all files in input folder
def main():
    for filename in os.listdir(input_folder):
        # Check if file is a .rpy file
        if filename.endswith('.rpy'):
            # Construct file paths
            input_file = os.path.join(input_folder, filename)
            backup_file = os.path.join(backup_folder, filename)
            output_file = os.path.join(output_folder, filename)

            # Create backup of input file
            shutil.copy2(input_file, backup_file)

            # Parse input file and write to output file
            with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
                state = STATE_NORMAL
                c = f_in.read(1)
                while c:
                    #print(f"Current state: {state_names[state]}")

                    if state == STATE_NORMAL:
                        # Check for open brackets
                        if c == '(':
                            state = STATE_IN_PARENS
                        elif c == '[':
                            state = STATE_IN_BRACKETS
                        elif c == '{':
                            state = STATE_IN_CURLY_BRACKETS
                        elif c == '"':
                            state = STATE_IN_QUOTE
                        elif c == '#':
                            state = STATE_COMMENT

                        # elif c == 'm':
                        #     if peek_n(f_in) == "enu:":
                        #         state = STATE_MENU



                        f_out.write(c)

                    # elif state == STATE_MENU:
                        
                    elif state == STATE_IN_PARENS:
                        # Check for close parenthesis
                        if c == ')':
                            state = STATE_NORMAL
                        f_out.write(c)
                    elif state == STATE_IN_BRACKETS:
                        # Check for close bracket
                        if c == ']':
                            state = STATE_NORMAL
                        f_out.write(c)
                    elif state == STATE_IN_CURLY_BRACKETS:
                        # Check for close curly bracket
                        if c == '}':
                            state = STATE_NORMAL
                        f_out.write(c)
                    elif state == STATE_IN_QUOTE:
                        # Check for close single quote
                        if c == '"':
                            state = STATE_NORMAL

                        elif c == '{':
                            prevstate = STATE_IN_QUOTE
                            #print(f"File position: {f_in.tell()}, character: {c}")
                            tag_peek = peek_until(f_in, '}')
                            print(tag_peek)
                            if re.match(WAIT_TAG_PATTERN, tag_peek):
                                state = STATE_IN_WAIT_TAG
                            else:
                                state = STATE_IN_QUOTE_TAG
                        elif c in PUNCTUATION_SINGLE:
                            if c == '-' and peek_n(f_in).isalnum():
                                state = STATE_IN_QUOTE
                            else: 
                                state = STATE_SINGLE_PUNCTUATION
                        elif c in PUNCTUATION_FULL:
                            if c == '.' and peek_n(f_in).isalnum():
                                state = STATE_IN_QUOTE
                            else:
                                state = STATE_DOUBLE_PUNCTUATION
                        
                        if state != STATE_IN_WAIT_TAG:
                            f_out.write(c)

                    elif state == STATE_IN_QUOTE_TAG:
                        if c == '}':
                            state = prevstate
                        f_out.write(c)

                    elif state == STATE_IN_WAIT_TAG:
                        if c == '}':
                            state = prevstate

                    elif state == STATE_SINGLE_PUNCTUATION:

                        if c == '{':
                            prevstate = STATE_SINGLE_PUNCTUATION
                            tag_peek = peek_until(f_in, '}')
                            # print(tag_peek)

                            if re.match(WAIT_TAG_PATTERN, tag_peek):
                                state = STATE_IN_WAIT_TAG
                            else:
                                state = STATE_IN_QUOTE_TAG
                                f_out.write(c)
                        
                        elif peek_n(f_in) not in PUNCTUATION_SINGLE:
                            
                            if c == '"':
                                f_out.write(c)
                                state = STATE_NORMAL
                            else:
                                if c == '\n':
                                    f_out.write('{w=0.4}')
                                    f_out.write(c)
                                else:
                                    f_out.write(c)
                                    f_out.write('{w=0.4}')
                                state = STATE_IN_QUOTE
                        else:
                            f_out.write(c)


                    elif state == STATE_DOUBLE_PUNCTUATION:

                        if c == '{':
                            prevstate = STATE_DOUBLE_PUNCTUATION
                            tag_peek = peek_until(f_in, '}')
                            # print(tag_peek)

                            if re.match(WAIT_TAG_PATTERN, tag_peek):
                                state = STATE_IN_WAIT_TAG
                            else:
                                state = STATE_IN_QUOTE_TAG
                                f_out.write(c)

                        elif peek_n(f_in) not in PUNCTUATION_FULL:
                            
                            if c == '"':
                                f_out.write(c)
                                state = STATE_NORMAL
                            else:
                                if c == '\n':
                                    f_out.write('{w=0.8}')
                                    f_out.write(c)
                                else:
                                    f_out.write(c)
                                    f_out.write('{w=0.8}')
                                state = STATE_IN_QUOTE
                        elif c == '.':
                            #f_out.write('{w=0.2}')
                            f_out.write(c)
                        else:
                            f_out.write(c)
                            

                    elif state == STATE_COMMENT:
                        f_out.write(c)
                        if c == '\n':
                            state = STATE_NORMAL
                    
                    
                    c = f_in.read(1)





    print('All files processed successfully.')



if __name__ == "__main__":
    main()