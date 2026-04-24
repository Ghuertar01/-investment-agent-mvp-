import json
from openai import OpenAI


SYSTEM_PROMPT = """
Eres un analista de inversiones prudente. Generas un Daily Investment Brief en español.
Reglas:
- No des asesoramiento financiero personalizado ni órdenes absolutas.
- Distingue entre hechos, señales, hipótesis y riesgos.
- Prioriza fuentes oficiales sobre foros y sentimiento OSINT.
- Incluye enlaces/fuentes cuando estén disponibles en los datos.
- Usa formato Markdown.
- Incluye un disclaimer al final.
- Propón señales: aumentar, mantener, reducir, vigilar o evitar.
- Incluye convicción: baja, media o alta.
- Incluye tamaño máximo sugerido como rango porcentual prudente, no como instrucción obligatoria.
"""


def generate_daily_brief(settings: dict, payload: dict) -> str:
    api_key = settings["env"].get("OPENAI_API_KEY")
    model = settings["env"].get("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        return fallback_report(payload, "OPENAI_API_KEY not configured")

    client = OpenAI(api_key=api_key)

    payload_text = json.dumps(payload, ensure_ascii=False, indent=2)[:50000]

    user_prompt = f"""
Genera un Daily Investment Brief con esta estructura:

# Daily Investment Brief — FECHA

## 1. Resumen ejecutivo
## 2. Macro
## 3. Fuentes oficiales y filings
## 4. Señales OSINT y sentimiento
## 5. Empresas bajo vigilancia
Tabla: Activo | Señal | Convicción | Motivo | Riesgo | Fuente
## 6. Ideas accionables prudentes
Tabla: Idea | Acción | Tamaño máx. sugerido | Horizonte | Condición de invalidación
## 7. Alertas del día
## 8. Qué NO hacer hoy
## 9. Disclaimer

Datos disponibles:
{payload_text}
"""

    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content


def fallback_report(payload: dict, reason: str) -> str:
    date = payload.get("generated_at", "")
    disclaimer = payload.get("portfolio_context", {}).get("disclaimer", "")
    payload_text = json.dumps(payload, ensure_ascii=False, indent=2)[:20000]

    return f"""# Daily Investment Brief — {date}

No se pudo generar el informe con LLM.

Motivo: `{reason}`

## Datos recogidos

```json
{payload_text}
```

## Disclaimer

{disclaimer}
"""
