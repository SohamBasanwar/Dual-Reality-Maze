from pathlib import Path
import json
R=Path(__file__).parent
report={'date':'2026-11-09','mainPort':'COM5','configuredI2CClockHz':100000,'tests':[], 'firmwareRemaining':'Temporary MainProbe, Probe_COM6 and Probe_COM8 diagnostics; production game firmware has NOT been restored.'}
for name in ['baseline-serial.txt','joystick-serial.txt','button-serial.txt']:
 if not (R/name).exists():continue
 rows=[]
 for line in (R/name).read_text(encoding='utf-8-sig').splitlines():
  try: rows.append(json.loads(line))
  except (ValueError,TypeError):pass
 for addr in [16,17]:
  s=[r for r in rows if r.get('addr')==addr]
  if not s:continue
  report['tests'].append({'file':name,'r3Port':'COM6' if addr==16 else 'COM8','diagnosticAddress':hex(addr),'samples':len(s),'valid':sum(r['valid'] for r in s),'echoOK':sum(r['echoOK'] for r in s),'txErrors':sum(r['tx']!=0 for r in s),'distinctSequenceValues':len({r['seq'] for r in s}),'xRange':[min(r['x'] for r in s),max(r['x'] for r in s)],'yRange':[min(r['y'] for r in s),max(r['y'] for r in s)],'buttonLowSamples':sum(bool(r['button']) for r in s),'finalXY':[s[-1]['x'],s[-1]['y']]})
report['limits']='Tests cover real I2C commands/echoes, CRC and joystick ADC inputs. They do not verify Wi-Fi, LCD, LEDs, buzzer, servo, production game integration or long-term reliability.'
(R/'TEST_RESULTS.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
