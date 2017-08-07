# Features
Import/Export .vcf vCard file via REST api
Search/Filter/Bulk Mark contacts

# Docker run example
```
docker run --name django-phone --net host -d fzinfz/django:phone python manage.py runserver 0:8000
docker exec -it django-phone python manage.py createsuperuser
```
then visit http://server_ip:8000

