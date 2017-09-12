# -*- mode: python -*-

block_cipher = None


a = Analysis(['GUI.py'],
             pathex=['/home/joonatoona/src/OpenMineMods'],
             binaries=[],
             datas=[('assets/*.svg', 'assets')],
             hiddenimports=['urllib3'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GUI',
          debug=False,
          strip=False,
          upx=True,
          console=True )
