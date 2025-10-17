PROMPT_TEMPLATE = """
Tu esi HR speciālists. Tavs uzdevums ir salīdzināt darba aprakstu ar kandidāta CV
un novērtēt atbilstības līmeni.

### Darba apraksts:
{jd_text}

### Kandidāta CV:
{cv_text}

Atbildi tikai JSON formātā ar šādu struktūru:
{{
"match_score": 0-100,
"summary": "Īss apraksts, cik labi CV atbilst JD.",
"strengths": ["Galvenās prasmes/pieredze no CV, kas atbilst JD"],
"missing_requirements": ["Svarīgas JD prasības, kas CV nav redzamas"],
"verdict": "strong match | possible match | not a match"
}}
"""