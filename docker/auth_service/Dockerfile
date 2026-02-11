FROM golang:1.22-alpine AS builder

WORKDIR /app

# installing git since it's needed for go modules sometimes
RUN apk add --no-cache git

COPY auth-service/go.mod auth-service/go.sum ./
RUN go mod download

COPY auth-service/ .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -o auth-server ./cmd/server

FROM alpine:3.19

WORKDIR /app

RUN adduser -D -H authuser

COPY --from=builder /app/auth-server /app/auth-server

USER authuser

EXPOSE 9100

CMD ["./auth-server"]