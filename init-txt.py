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
Inicjalizuje bazę danych Leśmianatora z pobranych plików TXT.

Skrypt pobiera paczkę plików TXT z utworami lirycznymi
i przekazuje ich treść Leśmianatorowi do analizy.

"""

from StringIO import StringIO
from urllib2 import urlopen
from zipfile import ZipFile

from lesmianator import Lesmianator


TXT_FILES = "http://www.wolnelektury.pl/media/packs/txt-liryka.zip"


if __name__ == '__main__':
    txt_zip = ZipFile(StringIO(urlopen(TXT_FILES).read()))

    poet = Lesmianator()
    for filename in txt_zip.namelist():
        print filename
        poet.add_txt_file(txt_zip.open(filename))

    poet.save()

