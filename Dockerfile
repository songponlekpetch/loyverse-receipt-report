FROM python:3.10.2-buster

ENV PYTHONUNBUFFERED True
ENV TZ Asia/Bangkok
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./

# RUN mkdir ~/.config
# RUN mkdir ~/.config/gspread
# RUN mv credentials/service_account.json ~/.config/gspread/service_account.json
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
