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

import json
import os
import logging
import datetime
from vobject import vCard
import vobject
import unicodedata


from contextlib import contextmanager

from django.db import transaction

from radicale.storage import BaseCollection, Item

from ..models import DBCollection, DBItem, DBProperties

from contacts.models import Contact

logger = logging.getLogger('djradicale')


class Collection(BaseCollection):
    main_collection_path = 'addressbook.vcf'
    user_collection_path = 'pim/odd/'

    def __init__(self, path, **kwargs):
        self.path = path # This is uuid
        # self.path = '/odd/'

    @classmethod
    def discover(cls, path, depth='0'):
        # for c in DBCollection.objects.filter(parent_path=path or ''):
        #     yield cls(c.path)
        #main_collection_path = 'addresses'
        #user_collection_path = 'pim/odd/'

        if depth != '0':
            for c in Contact.objects.filter(collection=path or ''):
                yield cls(cls.user_collection_path + cls.main_collection_path + c.path)

            if path == '/pim/':
                # yield cls(cls.user_collection_path + cls.main_collection_path)
                yield cls('odd')
                # return

            elif path == '/pim/.well-known/carddav':
                # yield cls(cls.user_collection_path + cls.main_collection_path)
                yield cls('odd')

            elif path == '/odd/':
                # yield cls('odd/' + main_collection_path)
                # yield cls(cls.user_collection_path + cls.main_collection_path)
                # yield cls(cls.main_collection_path)
                # yield cls(cls.user_collection_path + cls.main_collection_path)
                yield cls('odd')
            elif path == '/pim/odd/addressbook.vcf':
                # this_collection = os.path.basename(os.path.normpath(path))
                for c in Contact.objects.filter(collection=path + '/' or ''):
                    #yield cls(path + c.path)
                    yield cls(c.path)
        else:
            # # yield cls('odd/' + main_collection_path)
            # # if path == '/pim/.well-known/carddav':
            #     # yield cls(cls.user_collection_path + cls.main_collection_path)
            # if path == '/pim/odd/addressbook.vcf/':
            yield cls('pim/odd')
            yield cls('pim/odd/addressbook.vcf')
            # else:
                # yield cls('/odd/')
            for c in Contact.objects.filter(collection=path or ''):
                yield cls(c.collection + c.path)

                # yield cls(cls.user_collection_path + cls.main_collection_path)


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

        # yield 'addressbook.vcf'

        # TODO: Her hardkoder vi pathen foreløpig: os.path.dirname(self.path)
        # TODO: Finne ut av hvor denne path kommer fra?

        # this_collection = os.path.basename(os.path.normpath(self.path))
        # items = Contact.objects.filter(collection=self.path)
        items = Contact.objects.filter(path=self.path)
        for i in items:
            # yield i.collection + i.path
            yield i.path
            #yield self.user_collection_path + i.collection + '/' + i.path

    def get(self, href):
        # try:
        #     item = (
        #         DBItem.objects
        #         .filter(collection__path=self.path)
        #         .get(path=href))
        #     return Item(self, href=item.path, last_modified=self.last_modified)
        # except DBItem.DoesNotExist:
        #     pass

        #path = href

        #return Item(self, href='addressbook.vfc/addressbook', last_modified=self.last_modified, text=Contact.objects.latest('name').name)

        try:
            # item = (Contact.objects.filter(collection=self.path).get(path=href))
            # # return Item(self, href=item.path, last_modified=self.last_modified, text=item.name, item=item.vcard, name=item.name)
            # return Item(self, href=item.path, last_modified=self.last_modified, text=item.name, item=item.vcard, name="VCARD")

            # item_path = os.path.basename(href)
            # item = Contact.objects.filter(path=item_path).get()
            #item = Contact.objects.filter(path=href).get()
            #item = (Contact.objects.filter(collection=self.path).get(path=href))
            # return Item(self, href=item.path, last_modified=self.last_modified, text=item.name, item=item.vcard, name="VCARD")
            #return Item(self, href=item.path, last_modified=self.last_modified, text=item.name, item=item.vcard,name="VCARD")

            item_path = os.path.basename(self.path)
            #collection =
            item = (Contact.objects.filter(collection=self.path).get(path=href))
            return Item(self, href=item.path, last_modified=self.last_modified, text=item.name, item=item.vcard, name="VCARD")


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

        items = (Contact.objects.filter(collection=self.path).filter(path_in=hrefs))

        for item in items:
            yield item.path, Item(self, href=item.path, last_modified=self.last_modified, name="VCARD", etag=item.etag, text=item.vcard, vobject=item.vcard)

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

    def get_meta(self, key=None):
        if self.path == '/pim/odd/':
            # meta = 'addressbook.vcf'
            meta = '/odd/'
            #meta = json.loads('addressbook.vcf')

        else:
            if self.path == '/pim/odd/addressbook.vcf/':
                if key == 'tag':
                    meta = "VADDRESSBOOK"
                elif key == 'D:displayname':
                    meta = 'Odd-Henrik Addressbook'
                elif key == 'CR:supported-address-data':
                    #  <C:address-data-type content-type="text/vcard" version="3.0"/>
                    # https://tools.ietf.org/html/rfc6352#section-5.2
                    meta = 'text/vcard' # TODO: Hmm dette eller text/vcard??
                elif key is None:
                    # Todo: is this correct for collection?
                    recordname = os.path.basename(self.path)
                    p = Contact.objects.get(path=recordname)
                    meta = json.loads(p.vcard)

            elif self.path == '/pim/odd/':
                # Todo: Blir dette rett da?
                meta = self.path

            else:
                path = os.path.basename(self.path)
                #collection = os.path.dirname(self.path) + '/'


                # try:
                #     p = DBProperties.objects.get(path=self.path)
                #     meta = json.loads(p.text)
                #     if key is None:
                #         return meta
                #     else:
                #         return meta.get(key)
                # except DBProperties.DoesNotExist:
                #     pass

                try:
                    item = Contact.objects.get(path=path)
                    meta = json.loads(item.vcard)
                    if key is None:
                        return meta
                    else:
                        if key == 'tag':
                            return "VADDRESSBOOK"
                        elif key == 'D:displayname':
                            meta = item.name
                        elif key == 'CR:supported-address-data':
                        #  <C:address-data-type content-type="text/vcard" version="3.0"/>
                        # https://tools.ietf.org/html/rfc6352#section-5.2
                            meta = 'text/vcard'  # TODO: Hmm dette eller text/vcard??
                except Contact.DoesNotExist:
                    pass

                # # Vcard adress:
                # if key == 'tag':
                #     meta = "VADDRESSBOOK"
                # elif key == 'D:displayname':
                #     meta = 'Odd-Henrik Addressbook'
                # elif key == 'CR:supported-address-data':
                #     #  <C:address-data-type content-type="text/vcard" version="3.0"/>
                #     # https://tools.ietf.org/html/rfc6352#section-5.2
                #     meta = 'text/vcard'
                # elif key is None:
                #     # Todo: is this correct for collection?
                #     recordname = os.path.basename(self.path)
                #     p = Contact.objects.get(path=recordname)
                #     meta = json.loads(p.vcard)



            # if key == 'tag':
            #     if self.path == 'pim/odd/addresses/':
            #         meta = "VADDRESSBOOK"
            #     else:
            #         meta = "VCARD"
            #
            # elif key == 'D:displayname':
            #     meta = 'Odd-Henrik name'
            # elif key == 'CR:supported-address-data':
            #     #  <C:address-data-type content-type="text/vcard" version="3.0"/>
            #     # https://tools.ietf.org/html/rfc6352#section-5.2
            #     meta = 'text/vcard'
            # elif key is None:
            #     if self.path == '/pim/odd/':
            #         # meta = 'addressbook.vcf' # todo: bør dette kanskje være '/odd/'
            #         meta = self.path
            #
            #     else:
            #         recordname = os.path.basename(self.path)
            #         p = Contact.objects.get(path=recordname)
            #
            #         meta = json.loads(p.vcard)
            #         #meta = p.etag
            #

        return meta
        # try:
        #     p = DBProperties.objects.get(path=self.path)
        #     meta = json.loads(p.text)
        #     if key is None:
        #         return meta
        #     else:
        #         return meta.get(key)
        # except DBProperties.DoesNotExist:
        #     pass

    def set_meta(self, props):

        p, created = Contact.objects.filter(path=self.path)
        p.vcard = json.dump(props)
        p.save

        # p, created = DBProperties.objects.filter(path=self.path)
        # p.text = json.dumps(props)
        # p.save()

    def upload(self, href, vobject_item):
        # vobject_item.fn.value #Display name
        c, created = Contact.objects.get_or_create(path=href, collection='addressbook.vcf', vcard=vobject_item, name=vobject_item.fn.value)
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

