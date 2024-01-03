# AGH Class Divider

Projekt realizowany na przedmiot "Metodyki Projektów Teleinformatycznych" w roku 2022/2023

## Twórcy ✨

<table>
  <tbody>
    <tr>
        <td align="center" valign="top" width="14.28%"><a href="https://github.com/socheck"><img src="https://avatars.githubusercontent.com/u/56121251?v=4" width="100px;" alt="socheck"/><br /><sub><b>socheck</b></td>
        <td align="center" valign="top" width="14.28%"><a href="https://github.com/hbery"><img src="https://avatars.githubusercontent.com/u/44197723?v=4" width="100px;" alt="HBERY"/><br /><sub><b>hbery</b></td>
        <td align="center" valign="top" width="14.28%"><a href="https://github.com/agnieszkowe"><img src="https://avatars.githubusercontent.com/u/56120693?v=4" width="100px;" alt="agnieszkowe"/><br /><sub><b>agnieszkowe</b></td>
        <td align="center" valign="top" width="14.28%"><a href="https://github.com/krzysztofd1235"><img src="https://avatars.githubusercontent.com/u/56120661?v=4" width="100px;" alt="krzysztof1235"/><br /><sub><b>krzysztof1235</b></td>
    </tr>
        <tr>
        <td align="center" valign="top" width="14.28%"><a href="https://github.com/kowaleuro"><img src="https://avatars.githubusercontent.com/u/56120668?v=4" width="100px;" alt="kowaleuro"/><br /><sub><b>kowaleuro</b></td>
        <td align="center" valign="top" width="14.28%"><a href="https://github.com/wik-kwik"><img src="https://avatars.githubusercontent.com/u/67471556?v=4" width="100px;" alt="wik-kwik"/><br /><sub><b>wik-kwik</b></td>
        <td align="center" valign="top" width="14.28%"><a href="https://github.com/vvafwgsv"><img src="https://avatars.githubusercontent.com/u/56120588?v=4" width="100px;" alt="agnieszkowe"/><br /><sub><b>vvafwgsv</b></td>
    </tr>
  </tbody>
</table>

## Opis projektu 📚

Projekt zakłada stworzenie aplikacji webowej służącej do podziału studentów na grupy zajęciowe według zgłoszonych preferencji za pomocą formularza - użyte zewnętrzne narzędzia. Zestaw preferencji jest eksportowany do formatu .csv, który następnie jest możliwy do wgrania na aplikację. Aplikacja za pomocą autorskiego algorytmu dokonuje przydziałów studenta do slotów zajęciowych, tak by w jak największym stopniu trspełnić jego preferencje. Ostatecznie osoba korzystająca z aplikacji otrzymuje plik .csv z przydziałem każdego studenta do grupy zajęciowej.

## Użyte technologie i języki

### Frontend

- React JS

### Backend

- Python
- Fast Api

### Środowisko wirtualizacyjne

- Docker

## WorkFlow projektu

- [tutaj](_docs/WORKFLOW.md)

## Opis algorytmu/modelu matematycznego

- [tutaj](/_docs/ENGINE_MODEL.md)

## Uruchomienie aplikacji

Całość aplikacji podzielona jest na dwa kontenery dockerowe, odpowiednio jeden dla Frontend i jeden dla Backend. Plik konfigurujący całe środowisko znajduje się w pliku `docker-compose.yml`, który pozwala na uruchomienie aplikacji za pomocą komendy `docker-compose up` będąc w zasięgu pliku. Komenda wystawia na porcie lokalnym `3000`, możliwość podłączenia się do strony www aplikacji.

- [instalacja Docker](https://docs.docker.com/get-docker/)
- [instalacja Docker compose](https://docs.docker.com/compose/install/)

## Zestawy testowe

Znajdują się w katalogu `tests/data/suite_{1..3}`
