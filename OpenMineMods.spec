# -*- mode: python -*-

block_cipher = None


a = Analysis(['OpenMineMods.py'],
             pathex=['/home/joonatoona/src/OpenMineMods'],
             binaries=[],
             datas=[('LICENSE.txt', '.'),
                    ('CREDITS.md', '.')],
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
          console=False , icon='OMM.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='OpenMineMods')
