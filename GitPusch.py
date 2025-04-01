
import sys
import subprocess

def inputAndPull():
    do_pull = input("\033[32mCzy chcesz wykonać git pull? (T/ cokolwiek innego): \033[0m").upper()
    if do_pull in ('T'):
        print("\033[93mRobię GIT PULL\033[0m")
        subprocess.run(['git', 'pull' ], capture_output=True, text=True)
        print('KONIEC!')
        sys.exit()
    else:
        print("\033[93mNie robię GIT PULL\033[0m")
        print('KONIEC!')
        sys.exit()


print("\033[93mSprawdzam na jakim branchu jesteś\033[0m")
curent_branch = subprocess.run(['git', 'branch', '--show-current' ], capture_output=True, text=True)
print("Twój branch to: ",curent_branch.stdout.strip())

git_status = subprocess.run(['git', 'status', '--porcelain' ], capture_output=True, text=True)
if git_status.stdout.strip() != '':

    print("\033[91mNie są zakomitowane zmiany, dalszy proces zostaje zatrzymany.\033[0m")
    sys.exit()

if curent_branch.stdout.strip() == 'master':
    quick_fix_exist = subprocess.run(['git', 'branch', '--list', 'quick_fix' ], capture_output=True, text=True)

    print("\033[93mRobię GIT PULL\033[0m")
    subprocess.run(['git', 'pull' ], capture_output=True, text=True)
    
    if quick_fix_exist.stdout.strip() == '':
        print("Tworzę i przechodzę na branch quick_fix")
        subprocess.run(['git', 'checkout', '-b', 'quick_fix' ], capture_output=True, text=True)
    else:
        print("Przechodzę na branch quick_fix")
        subprocess.run(['git', 'checkout', 'quick_fix' ], capture_output=True, text=True)

    print("\033[93mŁączę mastera do quick_fixa\033[0m")
    subprocess.run(['git', 'merge', 'master' ], capture_output=True, text=True)
    print("Wysyłam do zdalnego repozytorium")
    subprocess.run(['git', 'push', 'origin', 'quick_fix' ], capture_output=True, text=True)
    print("\033[93mWracam na mastera\033[0m")
    subprocess.run(['git', 'checkout',  'master' ], capture_output=True, text=True)

    inputAndPull()

else:
    print("\033[93mWracam na mastera\033[0m")
    subprocess.run(['git', 'checkout',  'master' ], capture_output=True, text=True)
    print("Robię GIT PULL")
    subprocess.run(['git', 'pull' ], capture_output=True, text=True)
    print("\033[93mWracam na brancha " + curent_branch.stdout.strip() + " \033[0m")
    subprocess.run(['git', 'checkout',  curent_branch.stdout.strip() ], capture_output=True, text=True)
    print("Łączę mastera do " + curent_branch.stdout.strip() )
    subprocess.run(['git', 'merge', 'master' ], capture_output=True, text=True)
    print("\033[93mWysyłam do zdalnego repozytorium\033[0m")
    subprocess.run(['git', 'push', 'origin', 'quick_fix' ], capture_output=True, text=True)

    inputAndPull()

    


