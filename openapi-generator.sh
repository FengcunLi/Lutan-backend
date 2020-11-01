python manage.py generate_swagger swagger.yaml --overwrite --format yaml --url http://localhost:8000

rm -rf out/

docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
    -i /local/swagger.yaml \
    -g typescript-axios \
    -o /local/out/lutan-api
