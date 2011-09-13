Leśmianator
===========

To jest przykładowy projekt, który mógłby wystartować
w `Turnieju Elektrybałtów <http://turniej.wolnelektury.pl>`_. Jest napisany
w Pythonie, ale kluczowe elementy (zwłaszcza sposób dostępu do utworów
źródłowych w skryptach ``init-*.py``) powinny być zrozumiały również bez
znajomości tego języka.

Projekt zawiera właściwy program generujący wiersze (``lesmianator.py``)
i skrypty inicjalizujące (``init-*.py``) korzystające z różnych metod
dostępu do źródłowych utworów (API Wolnych Lektur, paczka z plikami TXT,
paczka z plikami XML). Zgłaszając się do Turnieju Elektrybałtów, wystarczy
oczywiście wybrać jedną z tych metod.


Zależności
----------

* Python 2.7
* Librarian (https://github.com/fnp/librarian)


Sposób użycia
-------------

Przed uruchomieniem Leśmianatora konieczne jest przeanalizowanie utworów
źródłowych przy pomocy jednego ze skryptów ``init-*.py``.

* ``init-api.py`` analizuje sonety Adama Mickiewicza, pobierając pliki tekstowe
  za pośrednictwem `API Wolnych Lektur <http://www.wolnelektury.pl/api>`_.
* ``init-txt.py`` analizuje wszystkie utwory liryczne, pobierając paczkę ZIP
  z plikami tekstowymi.
* ``init-xml.py`` analizuje wszystkie wiersze, pobierając paczkę ZIP
  z plikami XML i przetwarzając je za pomocą
  `librariana <https://github.com/fnp/librarian>`_.

Skrypt inicjalizacyjny zapisuje wyniki analizy utworów w pliku ``data.p``.

Na podstawie tych danych ``lesmianator.py`` generuje wiersz i wypisuje go
na standardowe wyjście.


Autorzy
-------

* Radek Czajka <radoslaw.czajka@nowoczesnapolska.org.pl>
