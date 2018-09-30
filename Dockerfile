FROM golang:latest 
RUN mkdir /app 
RUN go get github.com/gorilla/mux
ADD event.go handlers.go logger.go main.go order.go router.go routes.go /app/
WORKDIR /app 
RUN go build -o main
CMD ["/app/main"]
