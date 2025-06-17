# djsettings
“Smart enough” layout for Django project settings ... but not “too smart”.



## Project layout

Il progetto prevede:

- un folder `main` in cui viene conservato il progetto
- un folfer `myapp` che contiene una semplice applicazione
- `myapp` introduce il logger `logging.getLogger('myapp')` che verra' utilizzato per verificare il comportamento nel sistema di logging
- un semplice script `runtests.py`per eseguire gli unit test in modo controllato e prevedibile (ma senza introdurre ulteriori dipendenze)
- un folder locale di lavoro `data` escluso dal repository



Il database previsto di default e' SQlite, e precisamente "./data/db/db.sqlite3" per cui e' necessario garantire l'esistenza del folder "./data/db", anche se poi di fatto inutilizzato.

La maggior parte dei settings proposti da Django sono inutilizzati in questo progetto minimale, e possono essere commentati



## Settings files



I files relativi ai settings, raccolti in un unico modulo `main.settings` , hanno il ruolo di seguito descritto:

### setting.py

Contiene la lista di tutti i defaults del progetto, e viene di norma incluso da altri files che provvedono a integrarlo e/o fornire overrides di alcune variabili

### local.py

**Di norma non incluso nel repository**, e' il file utilizzato localmente per caratterizzare le necessita' della specifica istanza;

normalmente conterra' `DEBUG=False`(almeno in produzione) e le specifiche del database utilizzato dall'istanza.

Esempio minimale:

```python
from main.settings.settings import *

DEBUG = False
ALLOWED_HOSTS = ['*', ]

LOG_LEVEL = "DEBUG"
TRACE_SETTINGS_ENABLED = False
```

