import os
import json
import google.generativeai as genai

# Importē API atslēgu un prompta veidni
from config.api_key import API_KEY
from prompts.prompt_template import PROMPT_TEMPLATE

# Konfigurē Gemini
genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# =====================================
# Palīgfunkcijas
# =====================================

def read_file(path):
    """Nolasa teksta failu"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(content, path):
    """Saglabā teksta failu (piemēram, .md vai .txt)"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def write_json(data, path):
    """Saglabā JSON failu"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def generate_report(data):
    """Ģenerē Markdown pārskatu no JSON datiem"""
    md = f"""# Kandidāta novērtējums

**Atbilstības procents:** {data['match_score']}%

**Kopsavilkums:** {data['summary']}

## Stiprās puses:
"""
    for s in data['strengths']:
        md += f"- {s}\n"

    md += "\n## Trūkstošās prasmes:\n"
    for m in data['missing_requirements']:
        md += f"- {m}\n"

    md += f"\n**Verdikts:** **{data['verdict'].upper()}**\n"
    return md

# =====================================
# Gemini analīze
# =====================================

def analyze_with_gemini(jd_text, cv_text, prompt_path):
    """Izsauc Gemini Flash 2.5 modeli un saglabā prompt.md"""
    prompt = PROMPT_TEMPLATE.format(jd_text=jd_text, cv_text=cv_text)

    # Saglabā promptu failā
    write_file(prompt, prompt_path)

    # Izsauc modeli
    response = genai.GenerativeModel(MODEL_NAME).generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            response_mime_type="application/json"
        )
    )

    # Pārvērš atbildi par JSON
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print("Kļūda: modelis neatgrieza derīgu JSON. Lūk, atbilde:")
        print(response.text)
        return {"error": "Invalid JSON", "raw_response": response.text}

# =====================================
# Galvenā programma
# =====================================

def main():
    os.makedirs("sample_inputs", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    jd_path = "sample_inputs/jd.txt"
    if not os.path.exists(jd_path):
        print("Trūkst jd.txt faila mapē sample_inputs/. Izveido to un ieliec JD tekstu.")
        return

    jd_text = read_file(jd_path)

    for i in range(1, 4):
        cv_path = f"sample_inputs/cv{i}.txt"
        if not os.path.exists(cv_path):
            print(f"Trūkst {cv_path}. Izveido to un ieliec CV tekstu.")
            continue

        cv_text = read_file(cv_path)
        print(f"Analizē {cv_path}...")

        # Failu ceļi
        prompt_path = f"outputs/cv{i}_prompt.md"
        json_path = f"outputs/cv{i}.json"
        report_path = f"outputs/cv{i}_report.md"

        # Analīze
        result = analyze_with_gemini(jd_text, cv_text, prompt_path)

        # Saglabā rezultātus
        write_json(result, json_path)

        if "error" not in result:
            write_file(generate_report(result), report_path)
            print(f"Saglabāts: {prompt_path}, {json_path}, {report_path}")
        else:
            print(f"Kļūda analizējot {cv_path}")

    print("Visi faili saglabāti mapē outputs/")

# =====================================
# Izpilde
# =====================================

if __name__ == "__main__":
    main()
