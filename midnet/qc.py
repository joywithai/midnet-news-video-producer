from pathlib import Path
from .utils import ffprobe_json, run

def check(video,srt,thumbs,expected=(1920,1080)):
    issues=[]; info=ffprobe_json(video); vs=next((s for s in info['streams'] if s.get('codec_type')=='video'),None); aud=next((s for s in info['streams'] if s.get('codec_type')=='audio'),None)
    if not vs: issues.append('Video stream missing')
    elif (vs.get('width'),vs.get('height'))!=expected: issues.append('Unexpected resolution')
    if not aud: issues.append('Audio stream missing')
    if not Path(srt).exists() or Path(srt).stat().st_size<10: issues.append('Subtitle file missing or empty')
    if len(thumbs)!=3 or any(not Path(p).exists() for p in thumbs): issues.append('Three thumbnails were not created')
    decode=run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=False)
    if decode.returncode: issues.append('Full decode failed: '+decode.stderr[-500:])
    return {'status':'PASS' if not issues else 'FAIL','issues':issues,'video_stream':vs,'audio_stream':aud}
