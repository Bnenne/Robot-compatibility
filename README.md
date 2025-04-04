## About
This is a python program created by a member of the Informatics Subteam on FRC Team 1710. \
All data used in this project is taken from:\
Statbotics (https://www.statbotics.io/) \
The Blue Alliance (https://www.thebluealliance.com/) \
1710 Scouting (https://team1710scouting.vercel.app/), this is the website that the Informatics subteam on FRC Team 1710 creates in order to collect data on other FRC teams.

## Goal
The goal of this project is to create a program that can determine how compatible two robots are.\
However, this project is a **WORK IN PROGRESS** and the current compatibility score **DOESN'T** reflect the entire compatibility truth.

This project is intended to be used as an API route, but you can also use this frontend I created:\
https://compare.apibg.me/

## Use
Currently, the project has four routes with more to come:\
/auto/graph/{event}/{team} \
/auto/data/{event}/{team} \
/auto/compare/graph/{event}/{team1}/{team2} \
/auto/compare/graph/{event}/{team1}/{team2}/{team3}

/graph returns two graphs formatted on the 2024 FRC game blue alliance starting zone, one is every instance and the only shows the center of mass and average game pieces scored during the autonomous phase.\
/data returns the data as a dictionary. \
/compare/graph returns the same as /graph but for every team in the url. It also displays a graph with all the teams massed points and a graph with a compatibility score.

The routes only work for teams that have been scouting by Team 1710 and at competitions that Team 1710 has scouted at.\
If you put "events" for {event}, data for every competition that that team has been to in 2024 that 1710 has scouted will be returned.\
{event} should otherwise be the event ID formatted as the year followed by the event abbreviation (ex. 2024cttd), {team} should be formatted as "frc" followed by the team number (ex. frc1710).

## How it works
The current approach calculates a theoretical maximum by summing the highest average game pieces scored across starting positions for the teams. It also calculates a realistic maximum by considering practical constraints, such as assigning one robot per position and not reusing the same team. \
The compatibility score is the percentage of the theoretical maximum they're able to achieve with the realistic maximum.

## Try it out
Try visiting https://compare.apibg.me/auto/graph/events/frc1710 \
or **Auto** - **Graph** - **All 2024 Events** - **1710** via the front end \
https://compatibility.apibg.me/ \
You should get a graph like this:\
![example graph](https://cloud-2za8i7bzm-hack-club-bot.vercel.app/0frc1710.png)

### or

Try visiting https://compare.apibg.me/auto/compare/graph/events/frc1710/frc1730/frc1986 \
or **Auto** - **Compare** - **All 2024 Events** - **1710** - **1730** - **1986** via the front end \
https://compatibility.apibg.me/ \
You should get a graph like this:\
![example graph](https://cloud-h2vbe2hdh-hack-club-bot.vercel.app/0image.png)

The different colored points represent starting position groupings and the different sizes represent how many points were scored during the auto period when they started at that point.