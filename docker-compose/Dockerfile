FROM alpine
WORKDIR '/app'
COPY c3.c .
RUN apk add libc-dev
RUN apk add mpc1-dev 
RUN apk add gcc
RUN gcc c3.c
RUN ./a.out

