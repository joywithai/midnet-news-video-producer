from pathlib import Path
from PIL import Image
import json
IMAGE={'.png','.jpg','.jpeg','.webp'}; VIDEO={'.mp4','.mov','.mkv','.webm'}
def inventory(src_dir, sources_json=None):
    src=Path(src_dir); records=[]; metadata={}
    if sources_json and Path(sources_json).exists():
        try:
            for x in json.loads(Path(sources_json).read_text(encoding='utf-8')).get('assets',[]): metadata[x.get('filename','')]=x
        except Exception: pass
    for p in sorted(src.iterdir() if src.exists() else []):
        if p.name=='sources.json' or not p.is_file(): continue
        ext=p.suffix.lower(); kind='image' if ext in IMAGE else 'video' if ext in VIDEO else 'other'
        rec={'filename':p.name,'path':str(p.resolve()),'kind':kind,'archive':'archive' in p.stem.lower(),**metadata.get(p.name,{})}
        if kind=='image':
            try:
                with Image.open(p) as im: rec['width'],rec['height']=im.size
            except Exception as e: rec['error']=str(e)
        records.append(rec)
    return records
