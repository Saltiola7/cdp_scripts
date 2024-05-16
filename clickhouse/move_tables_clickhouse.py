import requests
from dotenv import load_dotenv


def query_clickhouse(sql, url, headers, auth, method='POST'):
    response = requests.request(method, url, data=sql, headers=headers, auth=auth)
    if response.text:
        return response.text.splitlines()
    else:
        return []

def move_tables(tables, source_db, target_db, clickhouse_config):
    auth = (clickhouse_config['username'], clickhouse_config['password'])
    for table in tables:
        create_sql = f"CREATE TABLE {target_db}.{table} AS {source_db}.{table};"
        insert_sql = f"INSERT INTO {target_db}.{table} SELECT * FROM {source_db}.{table};"
        drop_sql = f"DROP TABLE {source_db}.{table};"
        
        query_clickhouse(create_sql, clickhouse_config['url'], clickhouse_config['headers'], auth)
        query_clickhouse(insert_sql, clickhouse_config['url'], clickhouse_config['headers'], auth)
        query_clickhouse(drop_sql, clickhouse_config['url'], clickhouse_config['headers'], auth)

def main():
    load_dotenv('/Users/tis/foam/cdp/code/cfg/.env')
    clickhouse_config = {
        "url": "https://zzd2xg9oti.europe-west4.gcp.clickhouse.cloud:8443",
        "username": "default",
        "password": os.getenv('CLICKHOUSE_PASSWORD'),
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }
    tables = [
        "LVI_suunnittelija_Kumlinge_05_02_2024_", 
        "fi_cities", 
        "combined_meluton_data",
        "lvi_email_verification",
        "lvi_gmaps",
        "lvi_keywords",
        "lvi_missing_emails_domain_scrape",
        "lvi_programmatic_keywords",
        "lvi_programmatic_structures",
        "meluton_lvi_data_combined_1_",
        "meluton_lvi_data_sulvi"
    ]
    source_db = "default"
    target_db = "meluton"
    
    move_tables(tables, source_db, target_db, clickhouse_config)

if __name__ == "__main__":
    main()