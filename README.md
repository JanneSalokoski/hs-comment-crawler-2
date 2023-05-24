# HS-Crawler-2

Nappaa hesarin kommentit Exceliin 😎

## Käyttö

### Yhden artikkelin haku
Hakeaksesi yhden artikkelin, suorita `2 - Hae artikkeli` -pikakuvake. Ohjelma kysyy sinulta artikkelin osoitetta. Syötä sille osoite ja paina enteriä. Odota kunnes ohjelma on valmis. `Kommentit` -kansioon luodaan artikkelin otsikon mukainen excel-tiedosto, joka sisältää sen kommentit. Artikkelin osoite lisätään automaattisesti `artikkelit.txt` -tiedostoon.

Vaihtoehtoisesti voit suorittaa `hae_artikkeli.py` tai `get_article_async.py` python-tiedoston itse komentoriviltä tms. mutta pikakuvake on helppo ja kätsy.

### Kaikkien artikkeleiden haku
Hakeaksesi kaikki `artikkelit.txt` -tiedostossa esitetyt artikkelit, suorita `3 - Hae kaikki artikkelit` -pikakuvake. Ohjelma lukee kaikki tiedoston artikkelit, kerää niiden kommentit `Kommentit` -kansioon artikkeleiden omiin excel-tiedostoihin ja kokoaa kaikkien artikkeleiden kaikki kommentit yhteen `Kommentit/Kaikki kommentit.xlsx` -tiedostoon.

Tätä voi käyttää jo luettujen artikkeleiden päivittämiseen, tai useamman uuden artikkelin lukemiseen. Lukeaksesi useita uusia artikkeleita, lisää niiden osoitteet `artikkelit.txt` -tiedostoon omille riveilleen.

### Huomioita
Ohjelmaa ei voi käyttää, jos joku sen tarvitsemista tiedostoista on avattuna. Jos esimerkiksi `Kommentit/Kaikki kommentit.xlsx` on avattuna Excelissä, ohjelma kaatuu yritettäessä suorittaa kaikkien artikkeleiden hakua.

Artikkeleiden osoitteet tiedostossa `artikkelit.txt` käydään aina ohjelman ajettaessa läpi ja niistä poistetaan mahdolliset kaksoiskappaleet. Tiedostoon voi siis huoletta lisätä rivejä, ja ohjelma hoitaa loput.

## Asennus

1. Asenna Python: https://www.python.org/downloads/
2. Asenna pip: https://www.geeksforgeeks.org/how-to-install-pip-on-windows/
3. Asenna paketit: `py pip install selenium asyncio argparse logging tomllib`
4. Asenna Selenium ajuri: suorita `1 - Asenna` tai `install.py`