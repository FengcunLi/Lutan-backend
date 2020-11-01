export FAKER_LOCALE=zh_CN
python manage.py fakecategories 15

export FAKER_LOCALE=en
python manage.py fakecategories 15

export FAKER_LOCALE=zh_CN
python manage.py fakegroups 10
python manage.py fakeusers 100
python manage.py fakethreads 500
python manage.py fakeposts 1000

export FAKER_LOCALE=en
python manage.py fakegroups 10
python manage.py fakeusers 100
python manage.py fakethreads 500
python manage.py fakeposts 1000

python manage.py fakepostlikes 3000
python manage.py fakefollowings 500
