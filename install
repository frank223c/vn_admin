DEFAULT_USER="admin"
DEFAULT_EMAIL="admin@admin.com"
DEFAULT_PASS="admin"


# install gdal for spatial database capabilities
wget http://download.osgeo.org/gdal/1.11.2/gdal-1.11.2.tar.gz
tar xzf gdal-1.11.2.tar.gz
cd gdal-1.11.2
./configure
make # Go get some coffee, this takes a while.
sudo make install
cd ..

brew install mysql-connector-c
brew install openssl
pip3 install -r requirements.txt
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DEFAULT_USER', '$DEFAULT_EMAIL', '$DEFAULT_PASS')" | python manage.py shell --plain

