echo -n Password: 
read -s password
echo
# Run Command
python3 deploy_site.py "$password"
