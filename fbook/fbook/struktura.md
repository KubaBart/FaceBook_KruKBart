1.Profile
    -Unikalny profil
    -relacje (nadawca, odbiorce, status)
2.Posty
    -Posty
    -polubienia
    -komentarze
3.Uwierzytelnianie
    -rejestracja
    -wylogowywanie
    -logowanie
4.ogólne:
    -podzielenie na znajomych i nieznajomych
    -wyszukiwanie użytkownika po częściowym lub całościowym slug'u (specjalny identyfikator nadawany profilowi)
    -slug jest tworzony na postawie nazwy uzytkownika (w przypadku jeśli mamy podane imie i nazwisko slug przyjmuje taką postać np imie-nazwisko)
    -posty wyświetlane są według ilości like'ów oraz daty utworzenia
    -rozsuwane komentarze poprzez js
    -możliwość edytowania swoich danych (przy edycji imienia i nazwiska, zmienia się slug)
    -prywatność profili tzn. użytkownik nie będący znajomym nie może zobaczyć jego postów
    -na profilach użytkowników znajdują się ich posty, statystyki i dane
    -wyświetlanie postów na stronie głównej tylko i wyłącznie znajomych
    -edytowanie/usuwanie tylko swoich postów
    -po dodaniu postów/komentzów pojawia się na zielonym polu napis w stylu "dodano nowy komentarz/post"
    -liczniki komentarzy i polubień
    -w kodzie można zmienić ilość wyświetlanych komentarzy na stronie głównej (ograniczenia są zakomentowane na początku pliku posts/views.py)
    -po wejściu w zakładkę otrzymane zaproszenia można odrzucić albo przyjąć zaproszenie


Uwagi:
przy tworzeniu widoku wyszukiwania znajomych występował niezrozumiały błąd.
Reinstalacja, czyszczenie bazy nie pomagało, zatem metody zostały przeniesione do głównych widoków





w templates/main są przechowywane pliki html strony głównej i paska nawigacyjnego.
singals.py w profiles jest w pewnym sensie komunikacją.
w template plik base.html łączy pliki html które znajdują się w templates/html.
urls.py utworzyłem osobno dla profiles ponieważ składowanie wszystkich
adresów w fbook/urls.py mogłoby wyglądać bardzo nieestetycznie oraz w przypadku
błędu/pomyłki kosztować dużo czasu
