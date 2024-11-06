def create_files():
    from functions.team_actions import actions
    import json
    import csv

    team_intake_prev = []

    for t in actions:
        source = 0
        speaker = 0
        center = 0
        amp = 0
        trap = 0
        for i in t.get('actions').get('teleOp'):
            if i.get('action') == 'intake':
                if i.get('location') == 'source':
                    source += 1
                elif i.get('location') == 'speaker':
                    speaker += 1
                elif i.get('location') == 'center':
                    center += 1
                elif i.get('location') == 'amp':
                    amp += 1
                elif i.get('location') == 'trap':
                    trap += 1
        team_intake_prev.append({'team': t.get('team'), 'source': source, 'speaker': speaker, 'center': center, 'amp': amp, 'trap': trap})

    team_intake = []

    for t in actions:
        source = 0
        speaker = 0
        center = 0
        amp = 0
        trap = 0
        for i in t.get('actions').get('teleOp'):
            if i.get('action') == 'intake':
                if i.get('location') == 'source':
                    source += 1
                index = t.get('actions').get('teleOp').index(i)
                prev_action = t.get('actions').get('teleOp')[index - 1]
                if prev_action.get('action') == 'miss':
                    print(index)
                    print(t.get('actions').get('teleOp').index(prev_action))
                    print(i)
                    print(prev_action)
                    print(' ')
                    if prev_action.get('time') - i.get('time') > 5:
                        if i.get('action') == 'intake':
                            if i.get('location') == 'speaker':
                                speaker += 1
                            elif i.get('location') == 'center':
                                center += 1
                            elif i.get('location') == 'amp':
                                amp += 1
                            elif i.get('location') == 'trap':
                                trap += 1
        team_intake.append({'team': t.get('team'), 'source': source, 'speaker': speaker, 'center': center, 'amp': amp, 'trap': trap})

    with open("team_intake_prev.json", "w") as outfile:
        json.dump(team_intake_prev, outfile, indent=4)

    with open("team_intake.json", "w") as outfile:
        json.dump(team_intake, outfile, indent=4)

    with open('team_intake_prev.json') as f:
        data1 = json.load(f)

    # Open a CSV file for writing
    with open('team_intake_prev.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        # Write the header row (if the JSON data is an array of objects)
        if isinstance(data1, list):
            writer.writerow(data1[0].keys())

        # Write the data rows
        for row in data1:
            writer.writerow(row.values())

    with open('team_intake.json') as f:
        data2 = json.load(f)

    # Open a CSV file for writing
    with open('team_intake.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        # Write the header row (if the JSON data is an array of objects)
        if isinstance(data2, list):
            writer.writerow(data2[0].keys())

        # Write the data rows
        for row in data2:
            writer.writerow(row.values())