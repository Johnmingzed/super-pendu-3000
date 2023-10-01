python -m PyInstaller \
    --onedir --nowindow --noconsole \
    --add-data="README;." \
    --add-data="LICENSE;." \
    --add-data="app/data;data" \
    --add-data="app/src;src" \
    --icon="app/src/favicon.ico" \
    --name="SuperPendu3000" \
    app/main.py