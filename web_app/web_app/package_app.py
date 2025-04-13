import os
import sys
import shutil
import subprocess
import argparse
from datetime import datetime

def create_requirements_file():
    """Create a complete requirements.txt file for the application"""
    requirements = [
        "streamlit>=1.27.0",
        "pandas>=1.5.0",
        "numpy>=1.22.0",
        "openpyxl>=3.1.0",
        "beautifulsoup4>=4.11.0",
        "requests>=2.28.0",
        "matplotlib>=3.6.0",
        "wordcloud>=1.8.0",
        "pillow>=9.2.0",
        "pyinstaller>=5.6.0",  # For desktop packaging
    ]
    
    with open("requirements_full.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("✅ Created requirements_full.txt")
    return "requirements_full.txt"

def package_for_desktop(output_dir="dist"):
    """Package the application for desktop (Windows/macOS)"""
    print("📦 Packaging app for desktop...")
    
    # Create build directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine OS
    is_windows = sys.platform.startswith("win")
    is_mac = sys.platform.startswith("darwin")
    
    app_name = "News_Content_Downloader"
    
    if is_windows:
        print("🪟 Detected Windows OS")
        # Create a Windows executable using PyInstaller
        spec_file = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.streamlit', '.streamlit'),
        ('style.css', '.'),
        ('sources', 'sources'),
        ('README.md', '.'),
    ],
    hiddenimports=['streamlit', 'pandas', 'openpyxl', 'matplotlib', 'wordcloud'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
        
        # Write spec file
        with open(f"{app_name}.spec", "w") as f:
            f.write(spec_file)
        
        # Run PyInstaller
        subprocess.run([
            "pyinstaller",
            f"{app_name}.spec",
            "--clean",
            "--onefile",
            "--name", app_name
        ], check=True)
        
        # Create a batch file to run the app
        bat_content = f"""@echo off
echo Starting News & Content Downloader...
start "" "{app_name}.exe"
"""
        with open(os.path.join("dist", "Run_News_Downloader.bat"), "w") as f:
            f.write(bat_content)
            
        print(f"✅ Windows executable created at dist/{app_name}.exe")
        
    elif is_mac:
        print("🍎 Detected macOS")
        # Create a macOS app bundle using PyInstaller
        spec_file = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.streamlit', '.streamlit'),
        ('style.css', '.'),
        ('sources', 'sources'),
        ('README.md', '.'),
    ],
    hiddenimports=['streamlit', 'pandas', 'openpyxl', 'matplotlib', 'wordcloud'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{app_name}',
)

app = BUNDLE(
    coll,
    name='{app_name}.app',
    icon=None,
    bundle_identifier='com.newsdownloader.app',
    info_plist={{
        'NSHighResolutionCapable': 'True',
        'LSBackgroundOnly': 'False',
        'CFBundleDisplayName': 'News & Content Downloader',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    }},
)
"""
        
        # Write spec file
        with open(f"{app_name}.spec", "w") as f:
            f.write(spec_file)
        
        # Run PyInstaller
        subprocess.run([
            "pyinstaller",
            f"{app_name}.spec",
            "--clean",
            "--windowed",
            "--name", app_name
        ], check=True)
        
        # Create a shell script to run the app
        sh_content = """#!/bin/bash
echo "Starting News & Content Downloader..."
open "News_Content_Downloader.app"
"""
        with open(os.path.join("dist", "Run_News_Downloader.sh"), "w") as f:
            f.write(sh_content)
        # Make it executable
        os.chmod(os.path.join("dist", "Run_News_Downloader.sh"), 0o755)
            
        print(f"✅ macOS app bundle created at dist/{app_name}.app")
        
    else:
        print("❌ Unsupported operating system for desktop packaging")
        return False
    
    print("📦 Desktop packaging complete!")
    return True

def prepare_for_ios(output_dir="dist"):
    """Prepare files for iOS packaging with Pythonista or similar"""
    print("📱 Preparing files for iOS packaging...")
    
    ios_dir = os.path.join(output_dir, "ios_app")
    os.makedirs(ios_dir, exist_ok=True)
    
    # Copy necessary files
    files_to_copy = [
        "app.py", 
        "style.css", 
        "README.md"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, ios_dir)
    
    # Copy directories
    dirs_to_copy = ["sources"]
    
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(ios_dir, dir_name), dirs_exist_ok=True)
    
    # Create a modified version of app.py for iOS
    with open(os.path.join(ios_dir, "app.py"), "r") as f:
        app_content = f.read()
    
    # Add iOS-specific modifications
    ios_specific_code = """
# iOS-specific adjustments
import os
import sys

# Set up paths for iOS
if 'Pythonista3' in os.path.abspath(os.getcwd()):
    # We're running in Pythonista on iOS
    print("Running in Pythonista on iOS")
    # Create downloads directory in Pythonista documents
    downloads_dir = os.path.join(os.path.expanduser("~/Documents"), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    # Add the current directory to path to find modules
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
"""
    
    # Insert iOS-specific code after the imports
    modified_app_content = app_content.replace("import sys", "import sys\n" + ios_specific_code)
    
    with open(os.path.join(ios_dir, "app.py"), "w") as f:
        f.write(modified_app_content)
    
    # Create a README for iOS
    ios_readme = """# News & Content Downloader for iOS

## Installation Instructions

### Option 1: Using Pythonista 3
1. Download Pythonista 3 from the App Store
2. Copy all these files to your Pythonista documents folder
3. Install required packages using StaSh (Pythonista package manager)
4. Run app.py from Pythonista

### Option 2: Using Pyto
1. Download Pyto from the App Store
2. Copy all these files to your Pyto documents folder
3. Install required packages using Pyto's package manager
4. Run app.py from Pyto

### Required Packages
- streamlit
- pandas
- beautifulsoup4
- requests
- openpyxl

Note: Some features may be limited on iOS due to platform restrictions.
"""
    
    with open(os.path.join(ios_dir, "iOS_README.md"), "w") as f:
        f.write(ios_readme)
    
    # Create a zip file for easy download
    zip_filename = os.path.join(output_dir, f"News_Content_Downloader_iOS_{datetime.now().strftime('%Y%m%d')}.zip")
    shutil.make_archive(zip_filename[:-4], 'zip', ios_dir)
    
    print(f"✅ iOS package prepared at {zip_filename}")
    return zip_filename

def package_for_streamlit_cloud(output_dir="dist"):
    """Prepare files for deployment to Streamlit Cloud"""
    print("☁️ Preparing files for Streamlit Cloud...")
    
    cloud_dir = os.path.join(output_dir, "streamlit_cloud")
    os.makedirs(cloud_dir, exist_ok=True)
    
    # Copy necessary files
    files_to_copy = [
        "app.py", 
        "style.css", 
        "README.md"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, cloud_dir)
    
    # Copy directories
    dirs_to_copy = ["sources"]
    
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(cloud_dir, dir_name), dirs_exist_ok=True)
    
    # Create requirements.txt for Streamlit Cloud
    cloud_requirements = [
        "streamlit>=1.27.0",
        "pandas>=1.5.0",
        "numpy>=1.22.0",
        "openpyxl>=3.1.0",
        "beautifulsoup4>=4.11.0",
        "requests>=2.28.0",
        "matplotlib>=3.6.0",
        "wordcloud>=1.8.0",
        "pillow>=9.2.0",
    ]
    
    with open(os.path.join(cloud_dir, "requirements.txt"), "w") as f:
        f.write("\n".join(cloud_requirements))
    
    # Create a .streamlit folder with config.toml
    os.makedirs(os.path.join(cloud_dir, ".streamlit"), exist_ok=True)
    with open(os.path.join(cloud_dir, ".streamlit", "config.toml"), "w") as f:
        f.write("""[theme]
primaryColor = "#4CAF50"
backgroundColor = "#111111"
secondaryBackgroundColor = "#262730"
textColor = "#FFFFFF"
font = "sans serif"

[server]
headless = true
enableCORS = false
enableXsrfProtection = true
""")
    
    # Create a zip file for easy download
    zip_filename = os.path.join(output_dir, f"News_Content_Downloader_Cloud_{datetime.now().strftime('%Y%m%d')}.zip")
    shutil.make_archive(zip_filename[:-4], 'zip', cloud_dir)
    
    print(f"✅ Streamlit Cloud package prepared at {zip_filename}")
    return zip_filename

def main():
    parser = argparse.ArgumentParser(description="Package News & Content Downloader for various platforms")
    parser.add_argument("--platform", choices=["desktop", "ios", "cloud", "all"], default="all",
                      help="Platform to package for (desktop, ios, cloud, all)")
    parser.add_argument("--output", default="dist",
                      help="Output directory for packaged files")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Create requirements file
    requirements_file = create_requirements_file()
    
    # Package based on selected platform
    if args.platform in ["desktop", "all"]:
        package_for_desktop(args.output)
    
    if args.platform in ["ios", "all"]:
        prepare_for_ios(args.output)
    
    if args.platform in ["cloud", "all"]:
        package_for_streamlit_cloud(args.output)
    
    print("\n✨ Packaging complete! ✨")
    print(f"Output files are in the '{args.output}' directory")

if __name__ == "__main__":
    main() 