python generate_site.py


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
   firefox ../__deployed/index.html
fi
