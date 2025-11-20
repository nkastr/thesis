# Source on creating a docker image
# https://www.techrepublic.com/article/how-to-build-a-docker-image-and-upload-it-to-docker-hub/

# Variable definitions
docker_usr="nkastr"
token_path="./.token/docker-token.txt"

path_to_scheduler="./"
image_name="comm-aware-sc"  # also repo name
image_tag=41  # "latest"

# Get docker access token (you must create it and copy it to a txt file in that dir)
export TOKEN="$(cat ${token_path})"

# Connect to docker (--password-stdin ${token_path} might also work)
docker login --username ${docker_usr} --password ${TOKEN}

# Build the image
docker build -t ${image_name} ${path_to_scheduler}

# Wait for image to be created
# sleep 20

# Tag the image 
docker image tag ${image_name} ${docker_usr}/${image_name}:${image_tag}

# Push the image into a repository (repository must exist first)
docker image push ${docker_usr}/${image_name}:${image_tag}



