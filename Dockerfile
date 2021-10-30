FROM python:3.9-alpine

LABEL repository="https://github.com/shmileee/tabulate-action"
LABEL homepage="https://github.com/shmileee/tabulate-action"
LABEL maintainer="Oleksandr Ponomarov <ponomarov.aleksandr@gmail.com>"

LABEL com.github.actions.name="Display Infromation in a Table"
LABEL com.github.actions.description="A GitHub Action to display infromation in a table."

COPY src/requirements.txt /action/
RUN pip install --upgrade --force --no-cache-dir pip && pip install --upgrade --force --no-cache-dir -r /action/requirements.txt

COPY src/main.py /action/

ENTRYPOINT ["python", "/action/main.py"]
