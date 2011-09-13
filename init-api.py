#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2011 Fundacja Nowoczesna Polska
#
# This file is part of Leśmianator.
#
# Leśmianator is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leśmianator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Leśmianator.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Inicjalizuje bazę danych Leśmianatora na podstawie API Wolnych Lektur.

Skrypt za pomocą API wybiera wszystkie sonety Adama Mickiewicza,
pobiera ich treść w formacie TXT i przekazuje ją do analizy Leśmianatorowi.

"""

import json
from urllib2 import urlopen

from lesmianator import Lesmianator


API_BOOKS = "http://www.wolnelektury.pl/api/authors/adam-mickiewicz/genres/sonet/books"


def book_txt(url):
    book = json.load(urlopen(url))
    return book['txt']


if __name__ == '__main__':
    poet = Lesmianator()
    for book in json.load(urlopen(API_BOOKS)):
        print book['title']
        text_url = book_txt(book['href'])
        if text_url:
            poet.add_txt_file(urlopen(text_url))
    poet.save()

