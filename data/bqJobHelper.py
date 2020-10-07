# Please note you will need to configure and connect your BQ table to the appropriate destination
# This call assumes you have already completed configuration between machine and BQ. See: https://cloud.google.com/bigquery/docs/pandas-gbq-migration
# Please make sure your destination table has the following format:
# Field name	Type	Mode
# frame	INTEGER	NULLABLE	
# d_id	INTEGER	NULLABLE	
# left	INTEGER	NULLABLE	
# top	INTEGER	NULLABLE	
# right	INTEGER	NULLABLE	
# bottom	INTEGER	NULLABLE	
# video_name	STRING	NULLABLE	
# distance_alert	FLOAT	NULLABLE	
# center	STRING	NULLABLE	
# line	STRING	NULLABLE	

def push_to_bq(df):
    table_id = 'social_distancing.person_tracking'
    project_id = 'universal-stone-282519'
    df.to_gbq(destination_table=table_id, project_id=project_id, if_exists='append')