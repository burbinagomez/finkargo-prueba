FROM python:3.8-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV SECRET_KEY=0312c72bef44f2607baac5ba7f1f8a0a
RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev libffi-dev
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]