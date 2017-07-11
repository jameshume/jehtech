set -e 

if [ $# -ne 3 ] || [ "$2" != "onto" ]; then
	echo "### ERROR: invalid command line"
	exit 1
fi

if [ "$1" != "master" ] && [ "$1" != "new" ]; then
	echo "### ERROR: invalid command line"
	exit 1
fi

if [ "$3" != "master" ] && [ "$3" != "new" ]; then
	echo "### ERROR: invalid command line"
	exit 1
fi

REBASE_SRC=$1
REBASE_DEST=$3

rm -fr deleteme
mkdir deleteme
cd deleteme

echo -e "\n\nCREATING GIT REPO AND MASTER BRANCH"
git init

echo -e "\n\nMAKING FIRST MASTER COMMIT"
echo "master first" > master.txt
git add -A
git commit -m "First master commit"

echo -e "\n\nCREATING NEW FEATURE BRANCH"
git branch new


echo -e "\n\nMAKING SECOND MASTER COMMIT"
echo "master second" >> master.txt
git add -A
git commit -m "second master commit"

git log --oneline

echo -e "\n\nCREATING THE NEW FEATURE"
git checkout new
echo "first extra" >> new_feature.txt
git add -A
git commit -m "First new feature"
echo "second extra" >> new_feature.txt
git add -A
git commit -m "2 new feature"
echo "third extra" >> new_feature.txt
git add -A
git commit -m "3 new feature"
echo "fourth extra" >> new_feature.txt
git add -A
git commit -m "4 new feature"


echo -e "\n\nBRANCH AND LOG BEFORE REBASE"
git branch
git log --oneline


echo -e "\n\nREBASING $REBASE_SRC onto $REBASE_DEST"
git rebase "$REBASE_DEST" "$REBASE_SRC"

echo -e "\n\nBRANCH AND LOG  REBASE"FTER
git branch
git log --oneline


echo -e "\n\nMASTER LOG"
git checkout master
git log --oneline

echo -e "\n\nFEAURE LOG"
git checkout new
git log --oneline


