import platform
import subprocess
from pathlib import Path

for i in range(100):
    if platform.system() == 'Darwin':
        path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + \
               '/bin/ic20_darwin'
    elif platform.system() == 'Linux':
        path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + \
               '/bin/ic20_linux'
    else:
        path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + \
               '/bin/ic20_windows'
    subprocess.run(
        [path, '-u', 'http://localhost:' + str(5000) + '/collect', '-t', '0'],
        stdout=subprocess.DEVNULL)
