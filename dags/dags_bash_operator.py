import pendulum     #파이썬에서 제공하는 datetime 타입과 충돌을 피하기 위해 pendulum을 사용

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="dags_bash_operator", #DAG의 이름(고유 식별자) - 파이썬 파일명과는 무관하지만 일반적으로 동일하게 설정
    schedule="0 0 * * *",   #Cron 표현식으로 분, 시, 일, 월, 요일 순서로 스케줄 설정
    start_date=pendulum.datetime(2025, 11, 1, tz="Asia/Seoul"), #DAG 실행 시작 날짜 및 시간 설정
    catchup=False #DAG가 백필을 수행할지 여부 설정(False로 설정하면 백필 안함)(백필: DAG가 시작 날짜부터 현재 날짜까지의 모든 미실행된 스케줄을 실행하는 것)
    #dagrun_timeout=datetime.timedelta(minutes=60), #DAG 실행 시간 제한 설정(60분)
    #tags=["example", "example2"],   #tags 설정(대시보드에서 DAG를 필터링하는 데 사용, Optional)
    #params={"example_key": "example_value"},    #아래 dag 내에서 필요한 매개변수 설정(Optional)
) as dag:
    # Operator를 이용하여 bash_t1라는 Task 객체 생성
    bash_t1 = BashOperator(
        task_id="bash_t1",   #Dag의 Graph 내에서 보이는 Task의 이름(고유 식별자), Task 객체 이름과 무관하지만 일반적으로 동일하게 설정
        bash_command="echo whoami",    #실행할 bash 명령어 설정
    )

    bash_t2 = BashOperator(
        task_id="bash_t2",
        bash_command="echo $HOSTNAME",  #환경 변수 HOSTNAME 출력
    )

    bash_t1 >> bash_t2  #bash_t1이 완료된 후 bash_t2 실행되도록 설정