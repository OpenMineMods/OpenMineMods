# -*- mode: python -*-

block_cipher = None


a = Analysis(['Main.py'],
             pathex=['/home/joonatoona/src/OpenMineMods'],
             binaries=[],
             datas=[('Assets', 'Assets'),
                    ('LICENSE.txt', '.'),
                    ('CREDITS.md', '.'),
                    ('Assets/AutoUpdate', '.')],
             hiddenimports=['urllib3', 'PyQt5.uic.plugins', 'queue'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='OpenMineMods',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='OMM.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='OpenMineMods')
