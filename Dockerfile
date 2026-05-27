FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*


# Image metadata labels (from metadata.yml)
LABEL org.opencontainers.image.title="Cloud Native Task Management API"
LABEL org.opencontainers.image.description="Scalable cloud-native task management API built with Flask, Docker and AWS."
LABEL org.opencontainers.image.version="1.0.1"
LABEL org.opencontainers.image.license="MIT"
LABEL org.opencontainers.image.authors="Long"
LABEL org.opencontainers.image.source="cloud-native-task-management-api"
LABEL org.opencontainers.image.keywords="flask,docker,aws,mysql,gunicorn,devops,cloud-native"
LABEL io.platform.runtime.language="python"
LABEL io.platform.runtime.framework="flask"
LABEL io.platform.runtime.server="gunicorn"
LABEL io.platform.registry="aws-ecr"
LABEL io.platform.region="ap-southeast-1"


WORKDIR /app


RUN useradd -m appuser


COPY requirements.txt .


RUN pip install \
    --no-cache-dir \
    -r requirements.txt


COPY . .


RUN chmod +x entrypoint.sh


RUN chown -R appuser:appuser /app


USER appuser


EXPOSE 5000


CMD ["./entrypoint.sh"]
