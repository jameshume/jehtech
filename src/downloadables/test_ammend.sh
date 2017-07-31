rm -fr test_ammend
mkdir test_ammend
cd test_ammend

git init

echo "First line" > file.txt
git add -A
git commit -m "First commit about something"
echo "Second line with an error" >> file.txt
git commit -a -m "Second commit about something, with an error... oops"
echo "Third line" >> file.txt
git commit -a -m "Third commit about something"

git rebase -i HEAD~2