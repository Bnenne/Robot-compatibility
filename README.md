## About
This is a python program created by a member of the Informatics Subteam on FRC Team 1710. \
All data used in this project is taken from:\
Statbotics (https://www.statbotics.io/) \
The Blue Alliance (https://www.thebluealliance.com/) \
1710 Scouting (https://team1710scouting.vercel.app/), this is the website that the informatics team on FRC Team 1710 creates in order to collect data on other FRC teams.

## Goal
The goal of this project is to create a program that can determine how compatible two robots are.\
However, this project is a **WORK IN PROGRESS** and does **NOT** determine robot compatibility yet.\

This project is intended to be used as an API route, but you can also just directly access it:\
https://micro.apisb.me/graph/events/frc1710

## Use
Currently, the project has four routes:\
/graph/{event}/{team} \
/data/{event}/{team} \
/compare/graph/{event}/{team1}/{team2} \
/compare/graph/{event}/{team1}/{team2}/{team3}

/graph returns two graphs formatted on the 2024 FRC game blue alliance starting zone, one is every instance and the only shows the center of mass and average game pieces scored during the autonomous phase.\
/data returns the data as a dictionary. \
/compare/graph returns the same this as /graph but for every team in the url. I plan on adding two graphs that will give you insight on the teams' compatibility.

The routes only work for teams that have been scouting by Team 1710 and at competitions that Team 1710 has scouted at.\
If you put "events" for {event}, data for every competition that that team has been to in 2024 that 1710 has scouted will be returned./
{event} should otherwise be the event ID formatted as the year followed by the event abbreviation (ex. 2024cttd), {team} should be formatted as "frc" followed by the team number (ex. frc1710).

Try visiting https://micro.apisb.me/graph/events/frc1710 \
You should get a graph like this:\
![example graph1](https://micro.apisb.me/graph/events/frc1710)

or

Try visiting https://micro.apisb.me/compare/graph/events/frc1710/frc1730/frc1986 \
You should get a graph like this:\
![example graph2](https://micro.apisb.me/compare/graph/events/frc1710/frc1730/frc1986)

The different colored points represent starting position groupings and the different sizes represent how many points were scored during the auto period when they started at that point.