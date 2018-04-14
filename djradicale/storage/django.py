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

# http://localhost:8000/pim/odd/addressbook.vcf/

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
    tmpprops = '{"tag": "VADDRESSBOOK", "D:displayname": "GDPRAdressBook", "{http://inf-it.com/ns/ab/}addressbook-color": "#730bd5ff", "CR:addressbook-description": "GDPR Test AdressBook"}'

    def __init__(self, path, **kwargs):
        self.path = path # This is uuid
        # self.path = '/odd/'

    @classmethod
    def discover(cls, path, depth='0'):
        # for c in DBCollection.objects.filter(parent_path=path or ''):
        #     yield cls(c.path)

        principalCollection = Collection('pim/odd')
        principalCollection.is_principal = True

        MyCollection = Collection('pim/odd/addressbook.vcf')
        MyCollection.owner = 'pim/odd'
        MyCollection.is_principal = False






        if depth != '0':
            if path == '/pim/odd/':
                # yield MyCollection
                yield cls('pim/odd/addressbook.vcf')
                return

            if path == '/odd/':
                # yield principalCollection
                yield cls('pim/odd')
                return

            if path == '/pim/odd/addressbook.vcf/':
                # yield principalCollection
                # yield MyCollection

                # yield cls('pim/odd')
                yield cls('pim/odd/addressbook.vcf')

                for c in Contact.objects.filter(collection='addressbook.vcf' or ''):  # os.path.dirname(path)[1:]
                    # yield cls(c.collection + '/' + c.path)
                    j_vcard = json.loads(c.vcard)
                    vo_vcard = vCard()
                    vo_vcard = vobject.readOne(j_vcard)

                    yield  Item(cls,
                                  # collection=MyCollection,
                                  item=vo_vcard,
                                  href=c.path,
                                  last_modified=cls.last_modified,
                                  # text=str(vo_vcard),
                                  etag=c.etag,
                                  uid=c.uuid,
                                  name="VCARD",
                                  # name=c.name,
                                  # component_name='VCARD',
                                  )
                    # yield MyItem

                return

        else:
            return

    def get_meta(self, key=None):
        meta = {}

        if self.path == 'pim/odd':
            if key is None:
                pass

            elif key == 'CR:supported-address-data':
                    return '"text/vcard" version="3.0"'  # 'text/xml' vcard

            else:
                pass
                #return 'VADDRESSBOOK'


        else:
            meta = json.loads(self.tmpprops)
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
        #print('test')


        items = Contact.objects.filter(collection=os.path.basename(self.path))
        for i in items:
            yield i.path
        #except Contact.DoesNotExist:
        return

    # @property
    # def etag(self):
    #     """Encoded as quoted-string (see RFC 2616)."""
    #     # etag = md5()
    #     # for item in self.get_all():
    #     #     etag.update((item.href + "/" + item.etag).encode("utf-8"))
    #     # etag.update(json.dumps(self.get_meta(), sort_keys=True).encode())
    #     # return '"%s"' % etag.hexdigest()
    #     #
    #
    #     etag = md5()
    #     return etag

    def get(self, href):
        print('test')
        try:
            # if type(self.path) is str:
            item = os.path.basename(href)
            # collection = os.path.dirname(href) + '/'


            # else:
            #     item = href
            #     collection = os.path.dirname(self.path.href) + '/'

            # item = (Contact.objects.filter(collection=collection).get(path=item))
            c = (Contact.objects.get(path=href))
            j_vcard = json.loads(c.vcard)
            vo_vcard = vCard()
            vo_vcard = vobject.readOne(j_vcard)

            yield Item(
                self,
                # collection='/pim/odd/addresses/',
                item=vo_vcard,
                href=c.collection + c.path,
                last_modified=self.last_modified,
                # text=str(vo_vcard),
                etag=c.etag,
                uid=c.uuid,
                # name="VCARD",
                name=c.name,
                #component_name='component'
            )

        except Contact.DoesNotExist:
            pass


    def get_multi(self, hrefs):
        items = self.get_multi2(hrefs)
        if items:
            list(zip(*items))[1]

    def get_multi2(self, hrefs):
        # items = (
        #     DBItem.objects
        #     .filter(collection__path=self.path)
        #     .filter(path__in=hrefs))
        # for item in items:
        #     yield item.path, Item(self, href=item.path,
        #                           last_modified=self.last_modified)

        #yield ((href, self.get(href)) for href in hrefs)

        #collectionpath = os.path.dirname(self.path.href) + '/'

        items = Contact.objects.filter(collection=collectionpath)
        for i in items:
            j_vcard = json.loads(i.vcard)
            vo_vcard = vCard()
            vo_vcard = vobject.readOne(j_vcard)
            itempath = i.collection + i.path

            yield itempath, Item(
                self,
                # collection='/pim/odd/addresses/',
                item=vo_vcard,
                href=itempath,
                last_modified=self.last_modified,
                 text=str(vo_vcard),
                etag=i.etag,
                uid=i.uuid,
                name="VCARD",
                # name=i.name,
                #component_name=None
            )




        # files = None
        # for href in hrefs:
        #     # if files is None:
        #     #     # List dir after hrefs returned one item, the iterator may be
        #     #     # empty and the for-loop is never executed.
        #     path = self.path + href
        #     self.logger.debug(
        #         "Can't translate: %r", href)
        #     yield (href, None)
        #     #yield (href, self.get(href, verify_href=False))
        #
        #
        #     myhref = href
        #
        # collectionpath = os.path.dirname(self.path.href) + '/'
        # itemname = os.path.basename(self.path.href)
        #
        # items = (Contact.objects.filter(collection=collectionpath).filter(path_in=hrefs))

        # for item in items:
        #     yield item.path, Item(self, href=item.path, last_modified=self.last_modified, name="VCARD", etag=item.etag, text=item.vcard, vobject=item.vcard)

    def has(self, href):
        # return (
        #     DBItem.objects
        #     .filter(collection__path=self.path, path=href)
        #     .exists())

        return(
            Contact.objects
            .filter(collection=self.path, path=href)
            .exists())


    def delete(self, href=None):
        if href is None:
            DBItem.objects.filter(collection__path=self.path).delete()
            DBCollection.objects.filter(path=self.path).delete()
            DBProperties.objects.filter(path=self.path).delete()
        else:
            DBItem.objects.filter(
                collection__path=self.path, path=href).delete()

    def set_meta(self, props):

        p, created = Contact.objects.filter(path=self.path)
        p.vcard = json.dump(props)
        p.save

        # p, created = DBProperties.objects.filter(path=self.path)
        # p.text = json.dumps(props)
        # p.save()

    def upload(self, href, vobject_item):
        # vobject_item.fn.value #Display name
        c, created = Contact.objects.get_or_create(path=href, collection='addresses', vcard=vobject_item, name=vobject_item.fn.value)
        c.save()
        return c


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

