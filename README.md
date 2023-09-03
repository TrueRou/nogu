# nogu

osu! tournament practicing platform driven by modern python. In order to reduce the work in the progress of collecting data, sorting data and analyzing data.

---

## Aiming

Replace the position of Google / Tencent sheets.

Make everything in the match easier and relaxer

## Project Structure

- backend (nogu-nekko) -> services center, handle requests and inspection
- processor (nogu-nukko) -> data analysis and feedback
- frontend (nogu-zakko) -> represent data and analysis
- collector (nogu-pekko) -> collect realtime scores and spread data

## Project Stack

- backend: nogu-nekko with python, fastapi, sqlalchemy, mysql, and redis
- processor: nogu-nukko with csharp, redis
- frontend: nogu-zakko with vue, tailwindcss, and pinia
- collector: nogu-pekko with gosumemory, osu-sync

## Why "nogu"

"no" means keep away from something.

"gu" is a onomatopoeia in respect of the sound that doves make. In traditional China, "release white doves" means standing someone up.

"nogu" means keeping away from standing someone up (maybe your team leader, team member, or your favorite maps in the pool)

## What is nogu

nogu is a mixture composed of many parts relevant to osu!match including the solutions for match host, team leader and team member.

### Team

Create your own team and invite your friends to practice maps with you. Even bocchi(single-person) team is welcomed.

Team is a simple unit that unions your exercise pool and stages. Feel free to subscribe your interested map pool and analyze your performance.

### Map Pool

We consider a set of maps as map pool. You can even create a public styled-pool("lots of pps", "best streams", etc) for others for fun.

Usually, pools are for tournament, everyone are welcomed to create the pool of your tournament and shared it with stuff or other competitors

Pools can be subscribed by teams as "stage", Team owners can't modify the original pool but stage are ok. Stage can be considered as the ongoing instance of map pool.

When pools are updated by their owner, stages sourced from it can decide whether to sync with their upstream. It works like git repository

### Stage

Team often owns many stage but only one active stage. It is often the case that one single match has many stage (Qualifier, Semifinals, etc). They are designed from the thoughts of schedules.

Only scores matched to the active stage maps are recorded when submission. Don't betray your current loved maps when enjoying your exercises, lol.

### Maps

Maps are stand not only for "beatmap", but also for rules(mods, ruleset, etc) and formula(bancho, akatsuki, etc). So we consider maps as a larger concept.

We spot maps particularly by md5 instead of beatmap id, which means we can accept many version(older, old, new) of one single map. Uploaded offline maps are also welcomed.

import maps to create your map pool varies depends on your convenience. import from collection, sheets, image ocr are allowed just for convenience.


### Scores

Scores are not so that accurate and reliable in nogu because it costs. Fuzzy upload are welcomed. Nobody cares what the scores really like as long as analysis are relative accurate. You can describe what your score like instead of complex accurate data.

Of course, accurate scores are the right way. We support listening to the mplink or submit realtime scores by "collector". Our collector is based on osu memory reader such as gosumemory or osu-sync.

What's more, we even provide exercising server for you. They are individual private server specifically made for nogu services. Scores are automatically submitted if you are willing to access our private server.


### Private Server

Private server are built for all players who want immersive experience. We had made some special tweaks as nogu style.

Leaderboard are redesigned, global board will show scores made by your active team member, country board will show all your history scores made at current stage map.

Bots are special made for your convenience, suggesting you to play stage maps currently. Auto-hosted rooms are automatically running for you to practice your weakness.

### Collector

Collector combined with gosumemory running in the background when launched by player. Scores are listened and uploaded to nogu backend automatically through memory reader.

Surprisingly, headless client can also download maps that you need. All you need to do is subscribe your favorite pools through web. It works like steam workshop subscribe.

Thanks to URI, you can invite your team member running collector to multiplayer room directly without any clicking.


## Development

All the staff are still in development. Feel free to participate in the project.

## Roadmap

- Struct the whole project (Achieved: 2023.7.7)