FROM golang:1.13 AS build

ENV CGO_ENABLED=0
ENV GOOS=linux
ENV GO111MODULE=on

RUN go get github.com/gohugoio/hugo@v0.61.0 \
	&& go install github.com/gohugoio/hugo


# ---

FROM scratch

COPY --from=build /go/bin/hugo /hugo

ENTRYPOINT [ "/hugo" ]
