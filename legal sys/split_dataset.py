import json
import os

with open('indian_legal_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ipc = []
motor_vehicle = []
it_act = []
corruption = []
property_damage = []

for entry in data:
    act = entry.get('act', '').lower()
    crime = entry.get('crime', '').lower()
    
    if 'motor vehicles' in act:
        motor_vehicle.append(entry)
    elif 'information technology' in act:
        it_act.append(entry)
    elif 'prevention of corruption' in act:
        corruption.append(entry)
    elif 'public property' in act or 'mischief' in crime or 'property damage' in crime:
        property_damage.append(entry)
    elif 'penal code' in act:
        ipc.append(entry)
    else:
        # Default to IPC for anything else generic
        ipc.append(entry)

os.makedirs('datasets', exist_ok=True)

with open('datasets/ipc.json', 'w', encoding='utf-8') as f:
    json.dump(ipc, f, indent=2)
with open('datasets/motor_vehicle_act.json', 'w', encoding='utf-8') as f:
    json.dump(motor_vehicle, f, indent=2)
with open('datasets/it_act.json', 'w', encoding='utf-8') as f:
    json.dump(it_act, f, indent=2)
with open('datasets/corruption_act.json', 'w', encoding='utf-8') as f:
    json.dump(corruption, f, indent=2)
with open('datasets/property_damage.json', 'w', encoding='utf-8') as f:
    json.dump(property_damage, f, indent=2)

print("Split completed.")
