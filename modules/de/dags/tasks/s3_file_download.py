from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import os

def download_from_s3(key: str, bucket_name: str, local_path: str) -> str:
    """Download single file from s3 bucket and save it to `local_path`
    folder with random filename. Must exist AWS connection `s3_conn`.

    Parameters
    ----------
    key : str
        file path inside s3 bucket.
    bucket_name : str
        bucket name. e.g. `daredata-technical-challenge-data`.
    local_path : str
        local folder path where file will be saved with random name.

    Returns
    -------
    str
        local file path of the saved file with random name.
        e.g. `/var/tmp/airflow_tmp_77ln2tx0`
    """

    hook = S3Hook('s3_conn')

    file_name = hook.download_file(
        key=key,
        bucket_name=bucket_name,
        local_path=local_path
    )

    return file_name

def rename_file(ti, new_name: str, download_task_id: str) -> None:
    """Renames to `new_name` the random generated filename of the s3
    file that was downloaded in `download_task_id` task. Also change
    its permissions to allow PostgresOperator to read it later."""

    # get the random generated filename from XCOM
    downloaded_file_name = ti.xcom_pull(task_ids=[download_task_id])

    # rename file
    downloaded_file_path = '/'.join(downloaded_file_name[0].split('/')[:-1])
    os.rename(src=downloaded_file_name[0], dst=f"{downloaded_file_path}/{new_name}")

    # change file permission to allow PostgresOperator to read it later
    os.chmod(f"{downloaded_file_path}/{new_name}", 0o744)