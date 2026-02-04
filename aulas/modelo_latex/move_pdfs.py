from pathlib import Path
import shutil

# Diretório do projeto (onde o script está)
root_dir = Path(__file__).resolve().parent
build_dir = root_dir / "build"

if not build_dir.exists():
    raise FileNotFoundError("A pasta 'build' não existe.")

pdf_files = list(build_dir.glob("*.pdf"))

if not pdf_files:
    print("Nenhum arquivo PDF encontrado na pasta 'build'.")
else:
    for pdf in pdf_files:
        destination = root_dir.parent / pdf.name
        shutil.move(str(pdf), str(destination))
        print(f"Movido: {pdf.name}")

    print("Concluído.")

