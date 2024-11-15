import requests

data = []

r = requests.get('http://team1710scouting.vercel.app/api/2024wila/frc1710')
for e in r.json():
    data.append(e)

print(data)