import sys

print('start ...')

print('{ post_commands = ["cmd1", "cmd2"] }')

while True:
    command = sys.stdin.readline().rstrip('\n')
    if not command:
        break
    print command

    if command == '123':
        print('es funktioniert')