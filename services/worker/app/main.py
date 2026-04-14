from prometheus_client import start_http_server

from app.celery_app import celery_app

def main() -> None:
    start_http_server(9002)
    celery_app.worker_main(
        [
            "worker",
            "--loglevel=info",
        ]
    )

if __name__ == "__main__":
    main()