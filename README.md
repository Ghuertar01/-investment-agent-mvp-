# Investment Agent MVP — Daily Investment Brief

MVP automatizable para generar un informe diario de inversión usando fuentes oficiales, noticias y OSINT, y enviarlo por correo.

> Aviso: este proyecto genera información y análisis automatizados. No es asesoramiento financiero, legal ni fiscal.

## Qué hace

1. Consulta fuentes oficiales y públicas:
   - FRED para macroeconomía.
   - SEC EDGAR para filings recientes.
   - Reddit para OSINT de foros.
   - NewsAPI para noticias.
   - RSS opcional para fuentes oficiales y financieras.
2. Resume señales por activo, sector y macro.
3. Genera un Daily Investment Brief en Markdown.
4. Lo envía por email vía SMTP.

## Instalación

```bash
cd investment-agent-mvp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` con tus claves.

## Ejecutar manualmente

```bash
python main.py
```

El informe se guardará en `/reports` y se enviará por email si `SEND_EMAIL=true`.

## Programarlo con cron

Lunes a viernes a las 07:30:

```bash
30 7 * * 1-5 cd /ruta/investment-agent-mvp && /ruta/investment-agent-mvp/.venv/bin/python main.py >> cron.log 2>&1
```

## Ejecutarlo con GitHub Actions

Crea `.github/workflows/daily-brief.yml`:

```yaml
name: Daily Investment Brief

on:
  schedule:
    - cron: "30 6 * * 1-5"
  workflow_dispatch:

jobs:
  run-brief:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python main.py
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          FRED_API_KEY: ${{ secrets.FRED_API_KEY }}
          NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
          REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
          REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
          REDDIT_USER_AGENT: ${{ secrets.REDDIT_USER_AGENT }}
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
          SMTP_HOST: ${{ secrets.SMTP_HOST }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
          SEND_EMAIL: "true"
```

## Configuración

Edita `config.yaml` para cambiar activos vigilados, subreddits, fuentes RSS y perfil de riesgo.
