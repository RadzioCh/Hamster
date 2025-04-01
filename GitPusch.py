
import sys
import subprocess

# git branch --list quick_fix

print("\033[93mSprawdzam na jakim branchu jesteś\033[0m")
curent_branch = subprocess.run(['git', 'branch', '--show-current' ], capture_output=True, text=True)
print("Twój branch to: ",curent_branch.stdout.strip())

git_status = subprocess.run(['git', 'status' ], capture_output=True, text=True)

print(git_status.stdout.strip())
sys.exit()

if curent_branch.stdout.strip() == 'master':
    quick_fix_exist = subprocess.run(['git', 'branch', '--list', 'quick_fix' ], capture_output=True, text=True)
    if quick_fix_exist.stdout.strip() == '':
        print("Tworzę i przechodzę na branch quick_fix")
        subprocess.run(['git', 'checkout', '-b', 'quick_fix' ], capture_output=True, text=True)
        print("\033[93mŁączę mastera do quick_fixa\033[0m")
        subprocess.run(['git', 'merge', 'master' ], capture_output=True, text=True)
        print("Wysyłam do zdalnego repozytorium")
        subprocess.run(['git', 'push', 'origin', 'quick_fix' ], capture_output=True, text=True)
        print("\033[93mWracam na mastera\033[0m")
        subprocess.run(['git', 'checkout',  'master' ], capture_output=True, text=True)

else:
    print("not master")

print('KONIEC')