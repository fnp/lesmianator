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
Inicjalizuje bazę danych Leśmianatora z pobranych plików XML.

Skrypt pobiera paczkę plików XML, na podstawie metadanych wybiera te,
które należą do rodzaju "Liryka", za pomocą librariana przeprowadza
konwersję do postaci tekstowej, i tak uzyskany tekst przekazuje
Leśmianatorowi do analizy.

"""

from StringIO import StringIO
from urllib2 import urlopen
from zipfile import ZipFile

from librarian.dcparser import BookInfo
from librarian import text

from lesmianator import Lesmianator


XML_FILES = "http://www.wolnelektury.pl/media/packs/xml-all.zip"


if __name__ == '__main__':
    poet = Lesmianator()

    xml_zip = ZipFile(StringIO(urlopen(XML_FILES).read()))
    for filename in xml_zip.namelist():
        print filename
        info = BookInfo.from_file(xml_zip.open(filename))

        if u'Wiersz' in info.genres:
            output = StringIO()
            text.transform(xml_zip.open(filename), output, False, ('raw-text',))
            poet.add_text(output.getvalue())

    poet.save()

