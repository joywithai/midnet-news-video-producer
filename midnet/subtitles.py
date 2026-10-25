from pathlib import Path
import re
from .utils import media_duration

def ts(seconds):
    ms=round(seconds*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def sentence_chunks(text, max_words=11):
    words=text.replace('\n',' ').split(); chunks=[]; cur=[]
    for w in words:
        cur.append(w)
        if len(cur)>=max_words or re.search(r'[.!?]$',w): chunks.append(' '.join(cur)); cur=[]
    if cur: chunks.append(' '.join(cur))
    return chunks

def make_srt(script, audio, out):
    chunks=sentence_chunks(script)
    dur=media_duration(audio)
    weights=[max(2,len(c)) for c in chunks]; total=sum(weights) or 1; cursor=0.0; lines=[]
    for i,(c,w) in enumerate(zip(chunks,weights),1):
        span=dur*w/total; start=cursor; end=min(dur,cursor+span); cursor=end
        lines += [str(i),f'{ts(start)} --> {ts(end)}',c,'']
    Path(out).write_text('\n'.join(lines),encoding='utf-8')
    return {'segments':len(chunks),'duration':dur,'mode':'script-aligned proportional timing'}
