# nogu-nekko settings

debug = True
mysql_url = "mysql+aiomysql://root:password@localhost:3306/nogu"
jwt_secret = "nogu_debug"

# domain settings

bind_address = "127.0.0.1"
bind_port = 8000
prod_address = "https://nogu.dev/api"

# services settings

osu_api_v1_key = ""
osu_api_v2_id = 0
osu_api_v2_secret = ""
osu_api_v2_callback = ""


# tasks settings (in seconds)

beatmap_requests_interval = 0.5
match_inspection_interval = 10
match_inspection_each_interval = 0.1

