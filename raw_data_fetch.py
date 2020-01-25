import logging
import os

import boto3
import pandas as pd
from sqlalchemy import create_engine

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CONN_STRING = "{engine}://{username}:{password}@{host}:{port}/{db_name}"

def get_bucket_and_prefix_from_path(path):
    """
    Get the buckect and prefix from a given s3 path
    :param path: S3 dat path
    :return: bukect name and prefix
    """
    split_path = re.findall(r'[^\\/:*?"<>|\r\n]+', path)
    bucket = split_path[1]
    prefix = path[path.index(bucket) + len(bucket) + 1 :]

    return bucket, prefix


def _create_engine(engine, username, password, host, port, db_name):
    """
    Create enginer to query data
    :param engine: engine name
    :param username: database user name
    :param password: database user password
    :param host: host name
    :param port: port name
    :param db_name: database name
    :return:
    """
    connection_url = CONN_STRING.format(
        engine=engine, username=username, password=password, host=host, port=port, db_name=db_name
    )
    try:
        engine = create_engine(connection_url, pool_recycle=3600, echo=False, echo_pool=False)

        msg = CONN_STRING.format(
            engine=engine,
            username=username,
            password="*" * len(password),
            host=host,
            port=port,
            db_name=db_name,
        )
        logger.info("## {} engine created, connection: {}").format(engine, msg)

    except Exception as e:
        logger.info("## Unable to create engine.")
        logger.info(e)
        raise e
    return engine


def query_series_data_main():
    """
    This is the main function to query raw series data using Redshift Spectrum
    Firstly use ssm to get the credentials of database and user information
    Then create engine to connect with database and query the data
    :return:
    """
    ssm_client = boto3.client("ssm")
    credentials = ssm_client.get_parameters(
        Names=["toplinenn9_read_only_password", "toplinenn9_read_only_user"], WithDecryption=True
    )

    password = credentials["Parameters"][0]["Value"]
    username = credentials["Parameters"][1]["Value"]

    host = "toplinenn-9.c1twwlbaptvr.us-east-1.redshift.amazonaws.com"
    port = 8192
    db_name = "toplinenn9"
    Engine = "postgresql+pygresql"

    engine = _create_engine(Engine, username, password, host, port, db_name)
    connection = engine.connect()

    # This is the query sentence to pull raw series data,
    # You need to change the start date and end date, as well as target S3 bucket to upload the file

    sql = ('''
            UNLOAD($$
            WITH AFN AS
            (
                SELECT DISTINCT FULFILLMENT_MANAGER_ID
                FROM (
                        SELECT FULFILLMENT_MANAGER_ID FROM booker_ext.O_AFN_FULFILLMENT_MANAGER_ID
                        WHERE REGION_ID = 1 AND MARKETPLACE_ID IN(1)
                     )
                WHERE FULFILLMENT_MANAGER_ID IS NOT NULL
            ),
            DUCOI AS
            (
                SELECT DCOI.MARKETPLACE_ID, DCOI.REGION_ID,
                LEFT(FUNC_SHA1(DCOI.CUSTOMER_ID), 3) AS CUSTOMER_ID_GROUP, MAX(DCOI.ORDER_DAY) AS PURCHASE_DAY,
                SUM(DCOI.QUANTITY) AS PURCHASE_QUANTITY
                FROM booker_ext.D_UNIFIED_CUSTOMER_ORDER_ITEMS AS DCOI
                JOIN AFN ON AFN.FULFILLMENT_MANAGER_ID = DCOI.FULFILLMENT_MANAGER_ID
                WHERE DCOI.ORDER_DAY between '2014/01/01'::DATE and '2014/01/01'::DATE
                AND DCOI.ORDER_ITEM_LEVEL_CONDITION <> 6 AND DCOI.IS_FREE_REPLACEMENT = 'N'
                AND DCOI.MARKETPLACE_ID IN(1) AND DCOI.REGION_ID = 1
                AND DCOI.SHIP_OPTION NOT IN('Std Cont US Street Addr', 'download')
                GROUP BY DCOI.MARKETPLACE_ID, DCOI.REGION_ID, DCOI.CUSTOMER_PURCHASE_ID,
                LEFT(FUNC_SHA1(DCOI.CUSTOMER_ID), 3)
            )
            SELECT TO_CHAR(DUCOI.PURCHASE_DAY, 'YYYY/MM/DD') AS SNAPSHOT_DAY, CUSTOMER_ID_GROUP,
            SUM(1) AS  #Purchases, SUM(PURCHASE_QUANTITY) AS #OrderedUnits
            FROM DUCOI
            WHERE DUCOI.PURCHASE_DAY between '2014/01/01'::DATE and '2014/01/01'::DATE
            GROUP BY 1, 2
            $$)
            TO 's3://topline-nn-input-data/lizongy/raw_series_data/UPP_week_per_customer_id2019'
            HEADER
            FORMAT CSV
            IAM_ROLE 'arn:aws:iam::833872604190:role/MQCNNRedshiftIAMRole'
            KMS_KEY_ID '58febb23-f4c8-4805-b97f-5ecded4978d0'
            ENCRYPTED
            GZIP
            ALLOWOVERWRITE
            PARALLEL
            FALSE
        ''')
    logger.info("## Start to query data.")
    try:
        connection.execute(sql)
        logger.info("## Finished query data, and upload the raw series data to s3")
    except Exception as e:
        logger.info("## Unable to query data.")
        logger.info(e)
        raise e


