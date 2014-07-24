echo "Enter the new username:"
read name
echo "Enter the display text for this username:"
read display 
echo "Enter the password (carefully, will not be asked again):"
read passwd
python crypt_new.py -u $name -p $passwd -d $display
