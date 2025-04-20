# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['c:\\html\\dairy mangaement\\project/main.py'],
    pathex=[],
    binaries=[],
    datas=[('c:\\html\\dairy mangaement\\project/background.jpeg', '.'), ('c:\\html\\dairy mangaement\\project/background2.jpeg', '.'), ('c:\\html\\dairy mangaement\\project/database1.py', '.'), ('c:\\html\\dairy mangaement\\project/datbase2.py', '.'), ('c:\\html\\dairy mangaement\\project/datbase3.py', '.'), ('c:\\html\\dairy mangaement\\project/forgot.py', '.'), ('c:\\html\\dairy mangaement\\project/forgot1.py', '.'), ('c:\\html\\dairy mangaement\\project/info.py', '.'), ('c:\\html\\dairy mangaement\\project/login.py', '.'), ('c:\\html\\dairy mangaement\\project/mem.py', '.'), ('c:\\html\\dairy mangaement\\project/member.py', '.'), ('c:\\html\\dairy mangaement\\project/milk.py', '.'), ('c:\\html\\dairy mangaement\\project/register.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
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
