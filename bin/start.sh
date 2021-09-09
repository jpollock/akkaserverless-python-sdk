compile.sh
docker-compose -f docker-compose-proxy.yml down
docker-compose -f docker-compose-proxy.yml up -d
python index.py