# Analysis PRD

## Summary

analysis service is a part of nogu backend services, which works by python multiprocess

## Function

analysis service receives analysis requests through task queue.

when requests reach, it will extract required data from mysql

it then analyzes the data extracted and calculate for the final results

the final results will be saved to a few tables.

the message of process complete will also be inserted into another task queue

## Database Structure

### score_detail

- score_id: int (primary)
- slider_break_count: int
- stability: float
- confusion: float
- percentage: float
- message: str

### stage_detail

- stage_id: int (primary)
- play_count: int
- play_time: int

### stage_user_detail

- stage_id: int (primary)
- user_id: int (primary)
- play_count: int
- play_time: int
- harkworking_factor: float
- contribution_factor: float

### stage_map_detail

- stage_id: int (primary)
- beatmap_md5: str (primary)
- play_count: int
- play_time: int
- overall_performance: float
- prefer_factor: float

### stage_map_user_detail

- stage_id: int (primary)
- beatmap_md5: str (primary)
- user_id: int (primary)
- play_count: int
- play_time: int
- average_score: float
- average_accuracy: float
- average_stability: float
- average_percentage: float
- variance_score: float
- variance_accuracy: float

## Calculation Process

score_detail ->

stage_map_user_detail ->

stage_map_detail & stage_user_detail ->

stage_detail