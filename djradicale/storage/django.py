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
    tmpprops = '{"tag": "VADDRESSBOOK", "D:displayname": "GDPRAdressBook", "{http://inf-it.com/ns/ab/}addressbook-color": "#730bd5ff", "CR:addressbook-description": "GDPR Test AdressBook"}'

    def __init__(self, path, **kwargs):
        self.path = path # This is uuid
        # self.path = '/odd/'

    @classmethod
    def discover(cls, path, depth='0'):
        # for c in DBCollection.objects.filter(parent_path=path or ''):
        #     yield cls(c.path)

        principalCollection = Collection('odd')
        principalCollection.is_principal = True

        MyCollection = Collection('addressbook.vcf')
        MyCollection.owner = 'odd'
        MyCollection.is_principal = False




        if depth != '0':
            if path == '/odd/':
                yield principalCollection
                yield MyCollection
                return



            if path == '/pim/odd/addressbook.vcf':
                yield principalCollection
                yield MyCollection

                for c in Contact.objects.filter(collection='addressbook.vcf' or ''):  # os.path.dirname(path)[1:]
                    # yield cls(c.collection + '/' + c.path)
                    j_vcard = json.loads(c.vcard)
                    vo_vcard = vCard()
                    vo_vcard = vobject.readOne(j_vcard)

                    MyItem = Item(MyCollection,
                                  # collection=MyCollection,
                                  item=vo_vcard,
                                  href=c.path,
                                  last_modified=cls.last_modified,
                                  text=str(vo_vcard),
                                  etag=c.etag,
                                  uid=c.uuid,
                                  # name="VCARD",
                                  name=c.name,
                                  # component_name='component'
                                  )
                    yield MyItem

                return

        else:
            return



            #
            # return
            # MyCollection = Collection('addressbook.vcf')
            # # MyCollection.owner = principalCollection
            # yield MyCollection
            #
            # for c in Contact.objects.filter(collection=os.path.basename(path) or ''): #os.path.dirname(path)[1:]
            #     # yield cls(c.collection + '/' + c.path)
            #     j_vcard = json.loads(c.vcard)
            #     vo_vcard = vCard()
            #     vo_vcard = vobject.readOne(j_vcard)
            #
            #     MyItem=  Item(MyCollection,
            #                # collection=MyCollection,
            #                item=vo_vcard,
            #                href=(c.path)[1:],
            #                last_modified=cls.last_modified,
            #                text=str(vo_vcard),
            #                etag=c.etag,
            #                uid=c.uuid,
            #                # name="VCARD",
            #                name=c.name,
            #                # component_name='component'
            #                )
            #     yield MyItem
            #
            # return

            # elif path == '/pim/odd/addressbook.vcf':
            #
            #     MyCollection = Collection('addressbook.vcf')
            #     MyCollection.owner = 'odd'
            #     yield MyCollection

                # for c in Contact.objects.filter(collection=os.path.basename(path) or ''): #os.path.dirname(path)[1:]
                #     # yield cls(c.collection + '/' + c.path)
                #     j_vcard = json.loads(c.vcard)
                #     vo_vcard = vCard()
                #     vo_vcard = vobject.readOne(j_vcard)
                #
                #     MyItem=  Item(MyCollection,
                #                # collection=MyCollection,
                #                item=vo_vcard,
                #                href=(c.path)[1:],
                #                last_modified=cls.last_modified,
                #                text=str(vo_vcard),
                #                etag=c.etag,
                #                uid=c.uuid,
                #                # name="VCARD",
                #                name=c.name,
                #                # component_name='component'
                #                )
                #     yield MyItem
                # return

        #     elif path == '/pim/odd/addressbook.vcf/':
        #         return
        #
        #
        #     else:
        #         return
        #
        # # depth is 0:
        # else:
        #     if path == '/pim/odd/':
        #         MyCollection = Collection('addressbook.vcf')
        #         MyCollection.owner = 'odd'
        #         yield MyCollection
        #         return
        #     # principalCollection = Collection('/odd/')
        #     # principalCollection.is_principal = True
        #     # yield principalCollection
        #     #yield cls('/odd/')
        #     else:
        #         return

    def get_meta(self, key=None):
        meta = {}

        if self.path == 'odd':
            return 'MASTER'

        else:
            meta = json.loads(self.tmpprops)
            if key is None:
                return meta
            else:
                if key == 'CR:supported-address-data':
                    return 'text/vcard'  # 'text/xml' vcard
                else:
                    return meta.get(key)

        #
        #
        # if self.path == 'pim/odd':
        #     return
        #
        #     # meta = 'odd'
        #     # if key is None:
        #     #     return 'odd'
        #     # else:
        #     #     if key == 'CR:supported-address-data':
        #     #         return 'text/vcard'  # 'text/xml' vcard
        #     #     else:
        #     #         return 'odd'
        #
        # else:
        #     if self.path == 'odd/addressbook.vcf': # or self.path == 'pim/odd/addressbook.vcf/':
        #         meta = json.loads(self.addressbook_props)
        #         if key is None:
        #             return meta
        #         else:
        #             if key == 'CR:supported-address-data':
        #                 return 'text/vcard' # 'text/xml'
        #             else:
        #                 return meta.get(key)
        #
        #     else:
        #         # Get Card meta
        #         cardname = os.path.basename(self.path)
        #         card = Contact.objects.get(path=cardname)
        #
        #         jcard = json.loads(card.vcard)
        #         vo_vcard = vCard()
        #         vo_vcard = vobject.readOne(jcard)
        #
        #         meta = json.loads(card.vcard)
        #         if key is None:
        #             return meta
        #         elif key == 'CR:supported-address-data':
        #             return 'text/vcard'  # 'text/xml'
        #
        #         elif key == 'tag':
        #             return 'VADDRESSBOOK'
        #
        #         elif key == 'D:displayname':
        #             return card.name
        #
        #         else:
        #             return meta.get(key)

                # # SELF ISSTORAGE ITEM OBJECT??
                # meta = json.loads(self.addressbook_props) # addressbook_props
                # if key is None:
                #     return meta
                # else:
                #     # if key == 'tag':
                #     #     return 'VCARD'
                #     # elif key == 'CR:supported-address-data':
                #     #     return 'text/vcard'
                #     # else:
                #     return meta.get(key)




                # # path = os.path.basename(self.path)
                #
                # try:
                #     item_coll = os.path.dirname(self.path) + '/'
                #     item_path = os.path.basename(self.path)
                #     item = (Contact.objects.filter(collection=item_coll).get(path=item_path))
                #     # item = Contact.objects.get(path=self.path)
                #     meta = json.loads(item.vcard)
                #     if key is None:
                #         return meta
                #     else:
                #         if key == 'tag':
                #             return "VADDRESSBOOK" #"VADDRESSBOOK" # VCARD eller VADDRESSBOOK eller?
                #         elif key == 'D:displayname':
                #             meta = item.name
                #             #meta = 'VCARD'
                #         elif key == 'CR:supported-address-data':
                #             #  <C:address-data-type content-type="text/vcard" version="3.0"/>
                #             # https://tools.ietf.org/html/rfc6352#section-5.2
                #             meta = 'text/vcard'  # TODO: Hmm dette eller text/vcard eller xml??
                # except Contact.DoesNotExist:
                #     pass
                #
                # return meta

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
        if type(self.path) is str:
            collectionpath = self.path

        else:
            collectionpath = os.path.dirname(self.path.href)

        try:
            items = Contact.objects.filter(collection=collectionpath)
            for i in items:
                # yield i.collection + i.path
                yield i.path
                # yield self.user_collection_path + i.collection + '/' + i.path
        except Contact.DoesNotExist:
            pass


    def get(self, href):
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

        collectionpath = os.path.dirname(self.path.href) + '/'

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

