from pathlib import Path
import re

def _section(text, name, next_names):
    follows='|'.join(re.escape(n) for n in next_names)
    m=re.search(rf'(?ims)^#+\s*{re.escape(name)}\s*$\s*(.*?)(?=^#+\s*(?:{follows})\s*$|\Z)',text)
    return m.group(1).strip() if m else ''

def numbered(block):
    return [m.group(1).strip() for m in re.finditer(r'(?m)^\s*\d+[.)]\s*(.+)$',block)]

def parse_brief(path):
    text=Path(path).read_text(encoding='utf-8')
    full=_section(text,'Full News',['Photo / Resource Names','Thumbnail Ideas','Titles','Description'])
    english=_section(full,'English',['বাংলা অর্থ','Bengali Meaning','English'])
    bengali=_section(full,'বাংলা অর্থ',['Photo / Resource Names','Thumbnail Ideas','Titles','Description'])
    resources=numbered(_section(text,'Photo / Resource Names',['Thumbnail Ideas','Titles','Description']))
    thumbs=numbered(_section(text,'Thumbnail Ideas',['Titles','Description']))
    titles=numbered(_section(text,'Titles',['Description']))
    description=_section(text,'Description',['ZZZ_NEVER'])
    data={'english':english,'bengali':bengali,'resources':resources,'thumbnail_ideas':thumbs,'titles':titles,'description':description}
    errors=[]
    if len(english.split())<5: errors.append('English Full News is missing or too short.')
    if len(titles)!=3: errors.append('Exactly three titles are required.')
    if len(thumbs)!=3: errors.append('Exactly three thumbnail ideas are required.')
    if not description: errors.append('Description is missing.')
    data['validation_errors']=errors
    return data
