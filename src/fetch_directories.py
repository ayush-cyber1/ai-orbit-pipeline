import os
import json
from schema import new_entity

TOOLS = [
    ("MockItReal", "One design in, endless mockups out.", "https://mockitreal.com", "Product mockups"),
    ("Semaloop", "Catch mobile bugs before your users do.", "https://semaloop.com", "App testing"),
    ("Glean", "Work AI connected to your company's tools, data, and context.", "https://www.glean.com", "Personal assistant"),
    ("Kilo Code Reviewer", "AI-powered code reviews that catch bugs before merge.", "https://kilo.ai", "Code reviews"),
    ("TextSight.ai", "Detect AI content, then make it human.", "https://textsight.ai", "AI detection"),
    ("Ardelia", "Your AI company that runs while you sleep.", "https://www.getardelia.com", "Business operations"),
    ("Supernormal", "The AI assistant app that turns meetings into completed work.", "https://radiantapp.com", "Productivity"),
    ("Photo2Ads", "Turn one product photo into ads.", "https://photo2ads.com", "Video ads"),
    ("GeoCopy", "Get your brand cited in AI answers.", "https://geocopy.com", "SEO"),
    ("Kick", "Accounting software that does the work for you.", "https://kick.co", "Accounting"),
    ("Traccia", "AI Agent Control Plane.", "https://traccia.com", "AI observability"),
    ("Videnly", "Turn any idea into a complete YouTube video.", "https://videnly.com", "Videos"),
    ("Social Intents", "Real-time support and sales via messaging platforms.", "https://www.socialintents.com", "Customer support"),
    ("ChatPlayground AI", "The #1 platform for comparing AI models.", "https://www.chatplayground.ai", "LLM comparison"),
    ("Reglyph", "Translate the scan, keep the page.", "https://reglyph.com", "Document translation"),
    ("Katto", "One video in, every platform out.", "https://katto.tech", "Short videos"),
    ("Format Magic", "Format plain text into professional documents instantly.", "https://formatmagic.ai", "Document formatting"),
    ("Be The Book", "Turn someone you love into the star of their own book.", "https://bethebook.com", "Personalized books"),
]

def build_records(source_name, source_url):
    records = []
    for name, description, url, task in TOOLS:
        records.append(new_entity(
            "tools", name, description, url,
            ["Tools", task], source_name, source_url
        ))
    return records

def main():
    all_records = build_records("AI Directory", "https://theresanaiforthat.com")
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "directories_raw.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"saved {len(all_records)} -> {out_path}")

if __name__ == "__main__":
    main()