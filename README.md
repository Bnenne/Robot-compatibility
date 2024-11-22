This is a python program created by a member of the Informatics Subteam on FRC Team 1710.\
The goal of this project is to create a program that can determine how compatible two robots are.\
However, this project is a **WORK IN PROGRESS** and does **NOT** determine robot compatibility yet.\
All data used in this project is taken from:\
Statbotics (https://www.statbotics.io/) \
The Blue Alliance (https://www.thebluealliance.com/) \
1710 Scouting (https://team1710scouting.vercel.app/), this is the website that the informatics team on FRC Team 1710 creates in order to collect data on other FRC teams.

This project is intended to be used as an API route, but you can also access it here:\
https://micro.apisb.me/ \
or to have data returned try this:\
https://micro.apisb.me/graph/events/frc1710

Currently, the project has two routes:\
/graph/{event}/{team} \
/data/{event}/{team}

Graph returns a graph formatted on the 2024 FRC game blue alliance starting zone.\
Data returns the data as a dictionary.

The routes only work for teams that have been scouting by Team 1710 and at competitions that Team 1710 has scouted at.\
If you put "events" for {event}, data for every competition that that team has been to in 2024 that 1710 has scouted will be returned./
{event} should otherwise be the event ID formatted as the year followed by the event abbreviation (ex. 2024cttd), {team} should be formatted as "frc" followed by the team number (ex. frc1710).

Try visiting https://micro.apisb.me/graph/events/frc1710 \
You should get a graph like this:\
![example graph](https://cloud-efqh8dxue-hack-club-bot.vercel.app/0frc1710.png)

The different colored points represent starting position groupings and the different sizes represent how many points were scored during the auto period when they started at that point.