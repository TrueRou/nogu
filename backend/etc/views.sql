-- analyze stage map user
select
    s.user_id,
    s.beatmap_md5,
    count(s.id) as score_num avg(s.accuracy) as average_acc,
from
    osu_scores s
where
    stage_id = 1
group by
    s.user_id,
    s.beatmap_md5,
    s.stage_id