#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2010,2011 Fundacja Nowoczesna Polska
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
Leśmianator - program generujący wiersze na życzenie.

Wiersz generowany jest według następującego algorytmu:
Każdy kolejny znak jest losowany zgodnie z wyznaczoną wcześniej częstością
występowania znaków w tekstach źródłowych w kontekście trzech poprzednich
znaków.

Przykładowo, jeśli dotąd wygenerowaliśmy ciąg "Litw", to bierzemy pod uwagę
ciąg "itw". Jeśli w plikach źródłowych np. dwa razy pojawił się ciąg "itwo"
i raz ciąg "itwa", to kolejny znak losujemy między 'o' (z prawdopodobieństwem
2/3) a 'a' (z prawdopodobieństwem 1/3).

Wszystkie litery w plikach źródłowych są najpierw zamieniane na małe.
Białe znaki traktowane są tak samo, jak wszystkie pozostałe.

Leśmianator kończy pracę wraz z ukończeniem strofy (tj. wstawieniem pustej
linii), o ile napisał co najmniej dwa niepuste wersy (w przeciwnych przypadku
zaczyna kolejną strofę).

"""

from collections import Counter, defaultdict
from os.path import abspath, dirname, join
import cPickle as pickle
from random import randint
import re


class Lesmianator(object):

    SAMPLE_LENGTH = 3
    MIN_LINES = 2
    MAX_LEN = 1000

    DATA_FILE = join(dirname(abspath(__file__)), 'data.p')


    def __init__(self):
        self.continuations = defaultdict(Counter)

    def load(self):
        """Ładuje wyniki analizy z pliku."""
        with open(self.DATA_FILE) as f:
            self.continuations = pickle.load(f)

    def save(self):
        """Zapisuje wyniki analizy do pliku."""
        with open(self.DATA_FILE, 'w') as f:
            pickle.dump(self.continuations, f)

    def add_text(self, text):
        """Wykonuje właściwą analizę tekstu źródłowego.

        Zamienia tekst na małe litery i dla każdego znaku zapisuje, po jakim
        ciągu trzech znaków wystąpił.

        """
        last_word = ''
        text = unicode(text, 'utf-8').lower()
        for letter in text:
            self.continuations[last_word][letter] += 1
            last_word = last_word[-self.SAMPLE_LENGTH + 1:] + letter

    re_txt_file = re.compile(r'\n{3,}(.*?)\n*-----\n', re.S).search
    def add_txt_file(self, txt_file):
        """Dodaje plik tekstowy do analizy.

        Pliki tekstowe z Wolnych Lektur zawierają na początku nazwisko
        autora, tytuł i podtytuł utworu, następnie kilka pustych linii,
        tekst utworu i oddzieloną kreskami stopkę.  Funkcja wyciana z tego
        sam goły tekst i przekazuje go do właściwej analizy statystycznej.

        """
        m = self.re_txt_file(txt_file.read())
        self.add_text(m.group(1))

    def choose_letter(self, word):
        """Losuje kolejny znak wiersza."""
        if word not in self.continuations:
            return u'\n'

        choices = sum((self.continuations[word][letter]
                       for letter in self.continuations[word]))
        r = randint(0, choices - 1)

        for letter in self.continuations[word]:
            r -= self.continuations[word][letter]
            if r < 0:
                return letter

    def __call__(self):
        """Zwraca wygenerowany wiersz."""
        letters = []
        word = u''

        finished_stanza_verses = 0
        current_stanza_verses = 0
        verse_start = True

        char_count = 0

        # kończy pracę, jeśli ukończone strofy zawierają co najmniej
        # dwie niepuste linie
        while finished_stanza_verses < self.MIN_LINES and char_count < self.MAX_LEN:
            letter = self.choose_letter(word)
            letters.append(letter)
            word = word[-self.SAMPLE_LENGTH + 1:] + letter
            char_count += 1

            if letter == u'\n':
                if verse_start:
                    finished_stanza_verses += current_stanza_verses
                    current_stanza_verses = 0
                else:
                    current_stanza_verses += 1
                    verse_start = True
            else:
                verse_start = False

        return ''.join(letters).strip()


if __name__ == '__main__':
    poet = Lesmianator()
    poet.load()
    print poet()
