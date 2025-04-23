from setuptools import setup

APP = ['FocusTracker.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['rumps'],
    'includes': ['rumps', 'Foundation', 'objc', 'imp'],
    'frameworks':[
        '/Users/liusj/MyMiniConda/miniconda3/envs/myenv/lib/libffi.8.dylib'
    ],
    'plist': {
        'LSUIElement': True,
        'CFBundleName': 'FocusTracker',
        'CFBundleDisplayName': 'FocusTracker',
        'CFBundleIdentifier': 'com.user.focustracker',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
    },
}

setup(
    app=APP,
    name='FocusTracker',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
