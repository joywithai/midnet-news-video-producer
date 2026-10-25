import argparse
from pathlib import Path
from .pipeline import produce
def main():
    ap=argparse.ArgumentParser(description='Produce a MidNet News video package')
    ap.add_argument('--root',default='.')
    ap.add_argument('--input',default='input')
    ap.add_argument('--output',default='production')
    a=ap.parse_args(); r=produce(Path(a.root).resolve(),a.input,a.output); print(f"Production status: {r['status']}")
if __name__=='__main__': main()
