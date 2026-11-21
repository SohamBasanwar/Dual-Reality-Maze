"""Prepare the three named Arduino sketches and their shared protocol headers."""
from pathlib import Path
import argparse
import json
import re
import shutil
import textwrap
import zipfile

root = Path(__file__).resolve().parents[1]
metadata_path = root / 'hardware/submission-metadata.json'
parser = argparse.ArgumentParser()
parser.add_argument('--team-number')
args = parser.parse_args()
metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
if args.team_number:
    if not re.fullmatch(r'[A-Za-z0-9 -]{1,30}', args.team_number):
        raise ValueError('Use a short team number without comment delimiters.')
    metadata['team_number'] = args.team_number
    metadata_path.write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
assert len(metadata['abstract'].split()) == 100, 'The abstract must contain 100 words.'

destination = root / 'submission/Final_Arduino_Submission'
destination.mkdir(parents=True, exist_ok=True)
roles = {
    'Explorer': ('Arduino UNO R3', 'I2C peripheral at 0x10',
                 'Joystick X=A0, Y=A1, click=D2 to GND (INPUT_PULLUP);\n'
                 'Photoresistor divider=A2; SDA=A4; SCL=A5; common GND.'),
    'Architect': ('Arduino UNO R3', 'I2C peripheral at 0x11',
                  'Potentiometer wiper=A0; button=D2 to GND (INPUT_PULLUP);\n'
                  'Servo signal=D9; SDA=A4; SCL=A5; common GND.\n'
                  'Use a regulated servo supply with common ground for a loaded gate.'),
    'Main': ('Arduino UNO R4 WiFi', 'I2C controller; Wi-Fi access point and laptop bridge',
             'LCD=5V/GND/SDA/SCL; controller bus=A4/A5; RGB R=D9, G=D5, B=D3,\n'
             'one resistor per color; buzzer=D6; optional LED driver=D10.\n'
             'A4=SDA and A5=SCL on the same 5V bus; not the 3.3V Qwiic connector.')
}
for role, (board, function, pins) in roles.items():
    source = root / 'hardware/arduino-system' / role
    ino = source / f'{role}.ino'
    body = ino.read_text(encoding='utf-8-sig')
    marker = '/*\n * CS 362 - Project Submission Header\n'
    if body.startswith(marker):
        body = body.split(' */', 1)[1].lstrip('\r\n')
    lines = [
        'CS 362 - Project Submission Header',
        f"Team Number: {metadata['team_number']}".rstrip(),
        f"Project Name: {metadata['project']}",
        'Team Members (Name - NetID):',
        *[f"  {m['name']} - {m['netid']}" for m in metadata['members']],
        '', 'Abstract (100 words):',
        *textwrap.wrap(metadata['abstract'], width=77, break_long_words=False, break_on_hyphens=False),
        '', f'Sketch: {role}', f'Target board: {board}', f'Role: {function}',
        'Connections:', *pins.splitlines(),
        'Keep Protocol.h beside this sketch. All three boards share signal ground.'
    ]
    header = '/*\n' + '\n'.join(' * ' + line if line else ' *' for line in lines) + '\n */\n\n'
    ino.write_text(header + body, encoding='utf-8')
    folder = destination / role
    folder.mkdir(exist_ok=True)
    shutil.copy2(ino, folder / ino.name)
    shutil.copy2(source / 'Protocol.h', folder / 'Protocol.h')
    for extra in source.glob('*.h'):
        if extra.name != 'Protocol.h': shutil.copy2(extra, folder / extra.name)

number_note = ('Replace the team-number placeholder in all three headers before submission.\n'
               if metadata['team_number'].startswith('[') else '')
readme = f'''# {metadata['project']} - Arduino submission

Course: CS 362  
Team Number:{(' ' + metadata['team_number']) if metadata['team_number'] else ''}

{number_note}
| Member | NetID |
| --- | --- |
''' + '\n'.join(f"| {m['name']} | {m['netid']} |" for m in metadata['members']) + '''

Each .ino begins with the team number, every member's name and NetID,
project name, and the same 100-word abstract. The submission instructions
do not require working code; these files also include the project's current
implementation. Keep each Protocol.h next to its .ino; Main also needs CountdownBuzzer.h and MazeMatrix.h.

| Sketch | Board selection | Role |
| --- | --- | --- |
| Explorer/Explorer.ino | Arduino UNO | Joystick and photoresistor input; I2C address 0x10 |
| Architect/Architect.ino | Arduino UNO | Knob/button input and servo output; I2C address 0x11 |
| Main/Main.ino | Arduino UNO R4 WiFi | Poll controllers, drive LCD/RGB/buzzer, exchange laptop data |

Open each sketch separately in Arduino IDE. Board packages used for verification:
Arduino AVR Boards 1.8.8 and Arduino UNO R4 Boards 1.6.0.
Libraries: Servo 1.3.0 and hd44780 1.3.2. Wire and WiFiS3 are supplied by the board packages.
Select the correct physical board/port before uploading.

The laptop game and launcher remain in the main project folder; they are not
required dependencies for compiling these sketches and are not duplicated here.
The game's Reveal threshold is configured in the laptop adapter, not the Explorer
sketch: A2 below 1000 activates Reveal, and 1000 or above releases it.
The buzzer provides short countdown warnings at halfway, 3 and 2 minutes, then increasingly frequent warnings in the final minute.

Communication: Main polls both R3s over a shared wired I2C bus using different
addresses. The LCD shares that bus at its own address. Each R3 A4 goes to Main A4 (SDA),
each R3 A5 to Main A5 (SCL), and both grounds go to Main GND. Main's built-in Wi-Fi
connects to the laptop running the local game bridge.

Compilation and software checks do not verify wiring or mechanical operation.
See the project hardware/arduino-system/DEMO_QUICK_START.md for operation,
diagnostics, and the final physical check before demonstrating.
'''
(destination / 'README.md').write_text(readme, encoding='utf-8')
expected = {'README.md'} | {f'{r}/{name}' for r in roles for name in [f'{r}.ino', 'Protocol.h']}
expected.update({'Main/CountdownBuzzer.h','Main/MazeMatrix.h'})
actual = {p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}
assert actual == expected, f'Unexpected submission contents: {actual ^ expected}'
for file in destination.rglob('*'):
    if file.is_file():
        assert not re.search(r'\bAI\b|artificial intelligence|ChatGPT|OpenAI', file.read_text(encoding='utf-8'), re.I), file
zip_path = root / 'submission/Final_Arduino_Submission.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for file in sorted(destination.rglob('*')):
        if file.is_file():
            z.write(file, 'Final_Arduino_Submission/' + file.relative_to(destination).as_posix())
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
print(f'Prepared {destination}\nZIP: {zip_path}\nAbstract: 100 words\nTeam Number: {metadata["team_number"]}')
