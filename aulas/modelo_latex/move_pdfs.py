#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess

# Diretório do projeto (onde o script está)
root_dir = Path(__file__).resolve().parent
build_dir = root_dir / "build"
target_dir = root_dir.parent
compilar = False
gerar_uml = True


def compilar_tex(root_dir: str = ".", build_dir: str = "build"):
    root = Path(root_dir)
    build_dir = root / build_dir
    build_dir.mkdir(exist_ok=True)

    compilados = []
    for tex_file in root.glob("*.tex"):
        print(f"Compilando: {tex_file.name}")

        cmd = [
            "pdflatex",
            "-synctex=1",
            "--shell-escape",
            "-interaction=nonstopmode",
            f"-output-directory={build_dir}",
            tex_file.name
        ]

        subprocess.run(
            cmd,
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        compilados.append(tex_file.name.replace(".tex", ".pdf"))
    return compilados

def compilar_puml(root_dir: str = "."):
    root = Path(root_dir)

    compilados = []
    for tex_file in root.rglob("*.puml"):
        print(f"Compilando: {tex_file.name}")

        cmd = [
            "plantuml",
            tex_file.name
        ]

        subprocess.run(
            cmd,
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        compilados.append(tex_file.name.replace(".puml", ".pdf"))
    return compilados

#pdflatex -synctex=1 --shell-escape -interaction=nonstopmode -output-directory=build %.tex

if compilar:
    compilar_tex()

if gerar_uml:
    compilar_puml()

pdf_files = list(build_dir.glob("*.pdf"))

if not pdf_files:
    print("Nenhum arquivo PDF encontrado na pasta 'build'.")
else:
    for pdf in pdf_files:
        destination = target_dir / pdf.name
        shutil.move(str(pdf), str(destination))
        print(f"Movido: {pdf.name}")

    print("Concluído.")

