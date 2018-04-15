# Copyright (C) 2014 Okami, okami@fuzetsu.info

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

# http://localhost:8000/pim/odd/addressbook/

import json
import os
import logging
import datetime
from vobject import vCard
import vobject
import unicodedata
from radicale.storage import random_uuid4
from contextlib import contextmanager
from django.db import transaction
from radicale.storage import BaseCollection, Item
from ..models import DBCollection, DBItem, DBProperties
from contacts.models import Contact
from hashlib import md5

logger = logging.getLogger('djradicale')


class Collection(BaseCollection):

    def __init__(self, path, **kwargs):
        self.path = path # This is uuid

    @classmethod
    def discover(cls, path, depth="0"):
        # for c in DBCollection.objects.filter(parent_path=path or ''):
        #     yield cls(c.path)
        if depth != '0':

            if path == '/odd/' or path == '/pim/odd/addressbook/' or path == '/pim/odd/addressbook':
                # yield principalCollection
                principalcollection = cls('odd')
                principalcollection.configuration = cls.configuration
                yield principalcollection

                MyCollection = Collection('pim/odd/addressbook')
                MyCollection.configuration = cls.configuration
                yield MyCollection

                for c in Contact.objects.filter(collection='pim/odd/addressbook' or ''):  # os.path.dirname(path)[1:]
                    yield Item(MyCollection,
                                  # collection=MyCollection,
                                  item=json.loads(c.vcard),
                                  href=c.path,
                                  last_modified=cls.last_modified,
                                  text=json.loads(c.vcard),
                                  etag=c.etag,
                                  uid=c.uuid,
                                  name="VCARD",
                                  # name=c.name,
                                  component_name='VCARD',
                                  )
                return

        else:
            if path == '/pim/odd/addressbook/' or path == '/pim/odd/addressbook':
                MyCollection = Collection('pim/odd/addressbook')
                MyCollection.configuration = cls.configuration
                yield MyCollection

                for c in Contact.objects.filter(collection='pim/odd/addressbook' or ''):  # os.path.dirname(path)[1:]
                    thisItem = Item(MyCollection,
                                  # collection=MyCollection,
                                  item=json.loads(c.vcard),
                                  href=c.path,
                                  last_modified=cls.last_modified,
                                  text=json.loads(c.vcard),
                                  etag=c.etag,
                                  uid=c.uuid,
                                  name="VCARD",
                                  # name=c.name,
                                  component_name='VCARD',
                                  )

                    yield thisItem
                return

            else:
                MyCollection = Collection('pim/odd/addressbook')
                MyCollection.configuration = cls.configuration
                # yield MyCollection

                this_collection = os.path.dirname(path)
                this_item = os.path.basename(path)

                i = MyCollection.get(this_item)
                yield i



                # else:
                #     return

                # for c in Contact.objects.filter(collection=this_collection).get(paht=this_item):
                #     cls.get()
                #

    def get_meta(self, key=None):
        tmpprops = '{"tag": "VADDRESSBOOK", "D:displayname": "GDPRAdressBook", "{http://inf-it.com/ns/ab/}addressbook-color": "#730bd5ff", "CR:addressbook-description": "GDPR Test AdressBook"}'
        meta = {}

        if self.path == 'odd':
            if key is None:
                pass
            elif key == 'CR:supported-address-data':
                    return '"text/vcard" version="3.0"'  # 'text/xml' vcard
            else:
                pass

        else:
            meta = json.loads(tmpprops)
            if key is None:
                return meta
            else:
                if key == 'CR:supported-address-data':
                    return '"text/vcard" version="3.0"'  # 'text/xml' vcard
                else:
                    return meta.get(key)

    @classmethod
    def create_collection(cls, href, collection=None, props=None):
        print('CREATE')
        # c, created = DBCollection.objects.get_or_create(
        #     path=href, parent_path=os.path.dirname(href))
        # # if created:
        # #     p, created = DBProperties.objects.filter(path=href)
        # return c
        # TODO: CORRECT THIS:
        c, created = Contact.objects.get_or_create(path=href, collection=cls.user_collection_path + cls.main_collection_path)
        return c


    def list(self):
        # items = DBItem.objects.filter(collection__path=self.path)
        # for i in items:
        #     yield i.path
        #try:

        items = Contact.objects.filter(collection=self.path)
        for i in items:
            yield i.path
        #except Contact.DoesNotExist:
        return

    def get(self, href):
        try:
            c = Contact.objects.get(path=href)
            this_item = Item(self,
                                      # collection=MyCollection,
                                      item=json.loads(c.vcard),
                                      href=c.path,
                                      last_modified=self.last_modified,
                                      text=json.loads(c.vcard),
                                      etag=c.etag,
                                      uid=c.uuid,
                                      name="VCARD",
                                      # name=c.name,
                                      component_name='VCARD',
                                      )

            return this_item
        except Contact.DoesNotExist:
            return None


    def get_multi(self, hrefs):
        items = self.get_multi2(hrefs)
        if items:
            list(zip(*items))[1]

    def get_multi2(self, hrefs):
        ############# ORIGINAL CODE ######################################
        # items = (
        #     DBItem.objects
        #     .filter(collection__path=self.path)
        #     .filter(path__in=hrefs))
        # for item in items:
        #     yield item.path, Item(self, href=item.path,
        #                           last_modified=self.last_modified)
        #
        #yield ((href, self.get(href)) for href in hrefs)
        ###################################################################

        for h in hrefs:
            yield (h, self.get(h))

    def has(self, href):
        print('test')
        # # return (
        # #     DBItem.objects
        # #     .filter(collection__path=self.path, path=href)
        # #     .exists())
        #
        # return(
        #     Contact.objects
        #     .filter(collection=self.path, path=href)
        #     .exists())


    def delete(self, href=None):
        # TODO: There are probably more cases that needs to be handled here.
        coll = self.path
        itm = href
        # transaction.atomic()
        c = Contact.objects.filter(collection=coll, path=itm).delete()

    def set_meta(self, props):
        # TODO: Test and implement this
        p, created = Contact.objects.filter(path=self.path)
        p.vcard = json.dump(props)
        p.save

        # p, created = DBProperties.objects.filter(path=self.path)
        # p.text = json.dumps(props)
        # p.save()

    def upload(self, href, vobject_item):
        # TODO: Dette funker ikke helt som det skal, må få til redigering.
        c, created = Contact.objects.get_or_create(path=href,
                       collection='pim/odd/addressbook',
                       vcard=vobject_item,
                       name=vobject_item.fn.value,
                       # etag=str(href).replace('.vcf', ''),
                       )

        c.save()

        item = Item(self,
                    # collection=MyCollection,
                    item=vobject_item,
                    href=href,
                    last_modified=self.last_modified,
                    text=vobject_item,
                    etag=str(href).replace('.vcf', ''),
                    # uid=c.uuid,
                    name="VCARD",
                    # name=c.name,
                    component_name='VCARD',
                    )

        return item

    @property
    def last_modified(self):
        # try:
        #     collection = DBCollection.objects.get(path=self.path)
        # except DBCollection.DoesNotExist:
        #     pass
        # else:
        #     if collection.last_modified:
        #         return datetime.datetime.strftime(
        #             collection.last_modified, '%a, %d %b %Y %H:%M:%S %z')


        return datetime.datetime.strftime(Contact.objects.latest('last_modified').last_modified, '%a, %d %b %Y %H:%M:%S %z')


    @classmethod
    # @contextmanager
    def acquire_lock(cls, mode, user=None):
        return transaction.atomic()

