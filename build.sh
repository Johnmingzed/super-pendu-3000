python -m PyInstaller \
    --onefile --nowindow \
    --add-data="README.md:." \
    --add-data="LICENCE:." \
    --add-data="data:img" \
    app/main.py