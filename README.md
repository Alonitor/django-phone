# Features
- Import/Export .vcf vCard file via REST api
- Search/Filter/Bulk Mark contacts in Django Admin panel

# Docker run for demo
```
docker run --name django-phone --net host -d fzinfz/tools:django-phone python manage.py runserver 0:8000
docker exec -it django-phone /bin/bash
python manage.py createsuperuser
cd scripts
./vcard.py -i example.vcf -u  root -p your_password   # import sample vCards
```
Then visit 
- http://server_ip:8000
- http://server_ip:8000/api

# Import/Export contacts
Run `./scripts/vcard.py` for help.

