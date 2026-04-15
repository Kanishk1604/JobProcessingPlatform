from prometheus_client import start_http_server

from app.celery_app import celery_app

def main() -> None:
    start_http_server(9002)
    celery_app.worker_main(
        [
            "worker",
            "--loglevel=info",
            "--pool=solo",      #to maintain single main process instead of creating multiple child processes
        ]
    )

if __name__ == "__main__":
    main()