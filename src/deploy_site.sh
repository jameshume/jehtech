echo -n Password: 
read -s password
echo
# Run Command
python deploy_site.py "$password"
