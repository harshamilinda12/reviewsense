from pathlib import Path
folder=Path("data/raw")

for file in folder.iterdir():
    print(file.name,"|",file.suffix)

