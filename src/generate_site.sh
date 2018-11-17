#
# Usage ./generate_site.sh
# or    ./generate_site.sh <cmd>, where cmd is Python interpretter to use
RED='\033[1;31m'
NC='\033[0m'

CMD="$(which python)"
if [ $# -eq 1 ]; then
    CMD="$1"
    echo "Command forced to $CMD"
fi

if [ -z "$CMD" ]
then
    echo -e "\n\n${RED}###\n### No command found!\n###\n${NC}"
fi

echo "Using $CMD"
$CMD generate_site.py

if [ $? -eq 0 ]; then
    # From: https://unix.stackexchange.com/questions/9605/how-can-i-detect-if-the-shell-is-controlled-from-ssh
    MY_SESSION_TYPE=
    if [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ]; then
        MY_SESSION_TYPE=remote
        # many other tests omitted
    else
        case $(ps -o comm= -p $PPID) in
            sshd|*/sshd) MY_SESSION_TYPE=remote;;
        esac
    fi

    echo "Session type is \"$MY_SESSION_TYPE\""
    if [ "$MY_SESSION_TYPE" != "remote" ]; then
       echo "Launching browser..."
       firefox ../__deployed/index.html & disown
    fi
else
    echo -e "\n\n${RED}###\n### ERROR OCCURRED\n###\n${NC}"
fi

