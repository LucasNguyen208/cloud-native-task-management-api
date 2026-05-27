FROM python:3.13-slim


RUN apt-get update \
 && apt-get install -y curl \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /app


RUN useradd -m appuser


COPY requirements.txt .


RUN pip install \
    --no-cache-dir \
    -r requirements.txt


COPY . .


COPY entrypoint.sh .


RUN chmod +x entrypoint.sh


RUN chown -R appuser:appuser /app


USER appuser


EXPOSE 5000


CMD ["./entrypoint.sh"]
