@echo off
echo Checking for PyInstaller...
python -m pip install pyinstaller
if %errorlevel% neq 0 (
    echo Failed to install PyInstaller. Please check your Python installation.
    pause
    exit /b
)

echo.
echo Compiling HooverTron Application...
echo This may take a few minutes.
echo.

python -m PyInstaller --noconsole --onefile --icon=images/hoovertron_ico_file.ico --add-data "images;images" --name "HooverTron" main.py

if %errorlevel% equ 0 (
    echo.
    echo Compilation successful!
    echo The executable can be found in the "dist" folder.
) else (
    echo.
    echo Compilation failed. Please check the error messages above.
)

pause
