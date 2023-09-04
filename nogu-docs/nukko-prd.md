# nogu-nukko PRD

## Summary

nogu-nukko is a part of nogu backend services, which works at data analysis layer.

## Function

nukko receives analysis requests from nekko through redis task queue.

When requests reach, nukko will extract required data from mysql

nukko then analyzes the data extracted and calculate for the final results

The final results will be saved to redis.

The message of process complete will also be inserted into another redis task queue

## Database Structure

### analysis_requests

- stage_id: int (primary)
- timestamp: datatime

### analysis_response

- stage_id: int (primary)
- timestamp: datatime

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
- avarage_score: float
- avarage_accuracy: float
- avarage_stability: float
- avarage_percentage: float
- variance_score: float
- variance_accuracy: float

## Calculation Process

score_detail ->

stage_map_user_detail ->

stage_map_detail & stage_user_detail ->

stage_detail