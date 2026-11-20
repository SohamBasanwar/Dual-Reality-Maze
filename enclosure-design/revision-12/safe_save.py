"""Handle FreeCAD's Windows final-rename failure after a complete ZIP write."""
from pathlib import Path
import shutil, zipfile

def save_document(doc, target):
    target=Path(target)
    before=set(target.parent.glob(target.name+'.*'))
    try:
        doc.saveAs(str(target))
    except OSError:
        candidates=sorted(set(target.parent.glob(target.name+'.*'))-before,key=lambda p:p.stat().st_mtime,reverse=True)
        if not candidates: raise
        source=candidates[0]
        with zipfile.ZipFile(source) as archive:
            assert archive.testzip() is None
            assert 'Document.xml' in archive.namelist()
        shutil.copyfile(source,target)
        print('Recovered complete FreeCAD archive after final-rename failure:',target.name,flush=True)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
