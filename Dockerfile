FROM golang:latest 
RUN mkdir /app 
RUN go get github.com/gorilla/mux
RUN go get github.com/go-sql-driver/mysql
ADD event.go handlers.go logger.go main.go order.go router.go routes.go DatabaseHandler.go /app/
WORKDIR /app 
RUN go build -o main
CMD ["/app/main"]
