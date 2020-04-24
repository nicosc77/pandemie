import platform
import subprocess
from pathlib import Path

if platform.system() == 'Darwin':
    path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + \
           '/bin/ic20_darwin'
elif platform.system() == 'Linux':
    path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + \
           '/bin/ic20_linux'
else:
    path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + \
           '/bin/ic20_windows'

results = []
for i in range(10):
    process = subprocess.run([path, '-u',
                              'http://localhost:' + str(
                                  5000) + '/', '-t',
                              '0'],
                             encoding='utf-8',
                             stdout=subprocess.PIPE)
    if 'win' in str(process.stdout):
        results.append('win')
    elif 'loss' in str(process.stdout):
        results.append('loss')
wins = results.count("win")
losses = results.count("loss")
print('Completed test with following results: ' + str(
    wins / len(results) * 100) + '% win, ' + str(
    losses / len(results) * 100) + '% loss ')