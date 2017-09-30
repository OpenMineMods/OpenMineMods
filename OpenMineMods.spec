# -*- mode: python -*-

block_cipher = None


a = Analysis(['OpenMineMods.py'],
             pathex=['/home/joonatoona/src/OpenMineMods'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='OpenMineMods',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon='OMM.ico' )
app = BUNDLE(exe,
             name='OpenMineMods.app',
             icon='OMM.icns',
             bundle_identifier=None,
             info_plist={
                'NSHighResolutionCapable': True,
             },)
