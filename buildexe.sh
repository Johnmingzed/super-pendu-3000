python -m PyInstaller \
    --onefile --nowindow --noconsole \
    --add-data="README;." \
    --add-data="LICENSE;." \
    --add-data="app/data;data" \
    --add-data="app/src;src" \
    app/main.py