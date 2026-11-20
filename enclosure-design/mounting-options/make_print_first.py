from pathlib import Path
import csv,json
R=Path(__file__).resolve().parent;source=R.parent/'revision-09'/'fit-tests'
records=json.loads((source/'VALIDATION.json').read_text())
groups={'01':'A — Grip / battery trial','02':'A — Grip / battery trial','03':'A — Grip / battery trial','04':'B — I2C shutter trial','05':'B — I2C shutter trial','06':'B — I2C shutter trial','12':'C — USB shutter trial, if needed','13':'C — USB shutter trial, if needed','14':'C — USB shutter trial, if needed','20':'D — Optical pod trial','21':'D — Optical pod trial'}
with (R/'PRINT_FIRST.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['Batch','Existing fit-test file','Absolute path','Quantity for test','Purpose','Status'])
    for r in sorted(records,key=lambda r:r['file']):
        if r['file'][:2] not in groups:continue
        path=source/r['file'];assert path.is_file()
        w.writerow([groups[r['file'][:2]],r['file'],str(path),1,r['purpose'],'Prototype test only; not a final-print approval'])
print('11 existing test files listed in four batches; R09 geometry unchanged.')
