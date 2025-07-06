FROM golang:1.21-alpine
WORKDIR /app
COPY go.mod .
COPY main.go .
RUN go mod download
COPY . .
RUN go build -o content .
CMD ["./content"]
