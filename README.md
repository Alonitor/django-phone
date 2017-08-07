# Features
- Import/Export .vcf vCard file via REST api
- Search/Filter/Bulk Mark contacts in Django Admin panel

# Docker run for demo
```
docker run --name django-phone --net host -d fzinfz/django:phone python manage.py runserver 0:8000
docker exec -it django-phone python manage.py createsuperuser
```
Then visit 
- http://server_ip:8000
- http://server_ip:8000/api

# Import/Export contacts
Run `./scripts/vcard.py` for help.

