from pathlib import Path

path = Path('pi_million_digits.txt')
contents = path.read_text()

lines = contents.splitlines()
pi_string = ''
for line in lines:
    pi_string += line.strip()

birthday = input('Enter your birthday, in the form mmddyy: ')

if birthday in pi_string:
    print('Your birthday appears in the first million digits of pi!')
    
    position = pi_string.find(birthday)
    
    current_position = 0
    line_number = 0
    
    for i, line in enumerate(lines, 1):
        line_content = line.strip()
        current_position += len(line_content)
        if current_position > position:
            line_number = i
            break
    
    print(f'It appears at position {position} in the digits of pi.')
    print(f'It is located in line {line_number} of the file.')
    
else:
    print('Your birthday does not appear in the first million digits of pi.')