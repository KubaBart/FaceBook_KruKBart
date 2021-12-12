1.Profile
    -Unikalny profil
    -relacje (nadawca, odbiorce, status)
2.Posty
    -Posty
    -polubienia
    -komentarze
3.Uwierzytelnianie




w templates/main są przechowywane pliki html strony głównej i paska nawigacyjnego.
singals.py w profiles jest w pewnym sensie komunikacją.
w template plik base.html łączy pliki html które znajdują się w templates/html.
urls.py utworzyłem osobno dla profiles ponieważ składowanie wszystkich
adresów w fbook/urls.py mogłoby wyglądać bardzo nieestetycznie oraz w przypadku
błędu/pomyłki kosztować dużo czasu
