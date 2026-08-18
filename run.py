import subprocess

steps = [
    "fetch_github.py",
    "fetch_huggingface.py",
    "fetch_news.py",
    "fetch_youtube.py",
    "fetch_productsites.py",
    "fetch_directories.py",
    "clean.py",
    "normalize.py",
    "dedup.py",
    "classify.py",
    "enrich.py",
    "relationships.py",
    "validate.py",
]

for step in steps:
    print(f"\n--- running {step} ---")
    result = subprocess.run(["python", f"src/{step}"])
    if result.returncode != 0:
        print(f"{step} failed, stopping")
        break

print("\npipeline done")