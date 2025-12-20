# from youtube_dl import download_audio_temp
from transcribe import trancribe

# path = download_audio_temp('https://www.youtube.com/watch?v=WmnZB256B3w')
transc = trancribe('/tmp/tmp_9r1c70y.mp3')

with open('transcribe.json', 'w') as doc:
    doc.write(transc)