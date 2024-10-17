# Run Restack in Docker

docker run -d --pull always --name studio -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/engine:main

or

docker compose up -d --build --pull always

(will force repulling and rebuilding)

Restack UI will be available at http://localhost:5233
