# Creating a docker image of a scheduler to use it

# Steps based on:
# https://www.techrepublic.com/article/how-to-build-a-docker-image-and-upload-it-to-docker-hub/

# Some steps have to be done by hand and are skipped here

# Variable declarations
docker_usr="nkastr"
image_dir="../Code/dockerize"
image_name=""
image_tag="latest"

# Log into Docker Hub (you will be prompted to give a password, which should be a token that you create)
docker login -u ${docker_usr}  # kube-thesis

# Go into the directory with the desired Dockerfile
cd ${image_dir}

# Build your image
docker build -t ${image_name}

# Tag the image
docker image tag ${image_name} ${docker_usr}/${image_name}:${image_tag}

# Push the image to the repo
docker image push ${docker_usr}/${image_name}:${image_tag}

