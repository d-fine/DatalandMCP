#!/usr/bin/env bash
if ! grep -q "DatalandMCP" pyproject.toml; then
  echo "Please ensure that you call this script from the root of the python project (i.e., using ./bin/generate_dataland_api_clients.sh)"
  exit 1
fi

set -euxo pipefail
mkdir -p "./clients"

function openapi_generator() {
  if [ ! -f "./clients/openapi-generator-cli.jar" ]; then
    echo "OpenAPI Generator not found. Downloading..."
    curl https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.7.0/openapi-generator-cli-7.7.0.jar -o ./clients/openapi-generator-cli.jar
  fi
  java -jar ./clients/openapi-generator-cli.jar "$@"
}

# Dataland Backend
rm -rf ./clients/backend
openapi_generator generate \
    -i https://dataland.com/api/v3/api-docs/public \
    -g python \
    --additional-properties=packageName=dataland_backend \
    --type-mappings=date=str \
    -o './clients/backend'

# Dataland Document Manager
rm -rf ./clients/documents
openapi_generator generate \
    -i https://dataland.com/documents/v3/api-docs/public \
    -g python \
    --additional-properties=packageName=dataland_documents \
    --type-mappings=date=str \
    -o './clients/documents'

# Dataland QA Service
rm -rf ./clients/qa
openapi_generator generate \
    -i https://dataland.com/qa/v3/api-docs/public \
    -g python \
    --additional-properties=packageName=dataland_qa \
    --type-mappings=date=str \
    -o './clients/qa'

# Dataland Community Service
rm -rf ./clients/community
openapi_generator generate \
    -i https://dataland.com/community/v3/api-docs/public \
    -g python \
    --additional-properties=packageName=dataland_community \
    --type-mappings=date=str \
    -o './clients/community'
    
# Dataland User Service
rm -rf ./clients/users
openapi_generator generate \
    -i https://dataland.com/users/v3/api-docs/public \
    -g python \
    --additional-properties=packageName=dataland_users \
    --type-mappings=date=str \
    -o './clients/users'