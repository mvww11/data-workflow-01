FROM python:3.10
LABEL maintainer="Marcus Waddington"

COPY mle/mle_package /mle/mle_package
RUN pip install /mle/mle_package

COPY ds/ds_package /ds/ds_package
RUN pip install /ds/ds_package

RUN mkdir /models

COPY /deployment/api/entrypoint.sh /scripts/entrypoint.sh
ENTRYPOINT [ "/scripts/entrypoint.sh" ]