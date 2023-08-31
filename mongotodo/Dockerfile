FROM python:3-alpine3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt 

ENV PORT 5000

#expose http and mongodb ports
EXPOSE 5000 
EXPOSE 27017

CMD ["python", "./app.py"]
