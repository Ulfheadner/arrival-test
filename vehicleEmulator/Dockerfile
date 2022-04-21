FROM golang:1.12
RUN mkdir /consumer
ADD . /app/
WORKDIR /app
RUN go get "github.com/gorilla/websocket"
RUN go get "github.com/icrowley/fake"
RUN go build -o main .
CMD ["/app/main"]