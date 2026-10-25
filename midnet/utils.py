from pathlib import Path
import json, subprocess, shutil

def run(cmd, check=True):
    p=subprocess.run(cmd, text=True, capture_output=True)
    if check and p.returncode: raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr}")
    return p

def require(name):
    path=shutil.which(name)
    if not path: raise RuntimeError(f"Required executable not found: {name}")
    return path

def ffprobe_json(path):
    p=run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])
    return json.loads(p.stdout)

def media_duration(path):
    return float(ffprobe_json(path)['format']['duration'])

def write_json(path, obj):
    Path(path).write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
