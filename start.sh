pkill -f runserver
python3 manage.py runserver &
sleep 5
/usr/bin/open -a "/Applications/Google Chrome.app" 'http://localhost:8000/admin'