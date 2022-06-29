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
# call STRING NULLABLE	

import pandas as pd
from google.cloud import bigquery
from google.cloud import bigquery_storage

def push_to_bq(detections, video_name, call):
    for detection in detections:
        detection['video_name'] = video_name
        detection['call'] = call
    df = pd.DataFrame(detections)
    table_id = 'social_distancing.person_tracking'
    project_id = 'universal-stone-282519'
    df.to_gbq(destination_table=table_id, project_id=project_id, if_exists='append')

def video_analyzed(video_name, call):
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT COUNT(video_name)
        FROM `universal-stone-282519.social_distancing.person_tracking` 
        WHERE video_name = '""" + video_name + """' AND call = '""" + call + """'
        """
    )

    results = query_job.result()  # Waits for job to complete.
    
    for row in results:
        video_results = row.f0_
        #print("{} : {} views".format(row.url, row.view_count))
    
    if video_results > 0: return True 
    else: return False

def pull_from_bq(video_name, call):
    client = bigquery.Client()
    storageClient = bigquery_storage.BigQueryReadClient()
    query_string = """
    SELECT *
    FROM `universal-stone-282519.social_distancing.person_tracking` 
    WHERE video_name = '""" + video_name + """' AND call = '""" + call + """'
    """
    df = (
        client.query(query_string)
        .result()
        .to_dataframe(bqstorage_client=storageClient)
    )
    df = df.sort_values(by=['frame']) # Sort by Frame
    detections = df.to_dict('records')
    return detections