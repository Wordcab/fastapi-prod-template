<h1 align="center">Wordcab Transcribe</h1>
<p align="center"><em>Example Project</em></p>

<div align="center">
	<a  href="https://github.com/Wordcab/wordcab-transcribe/releases" target="_blank">
		<img src="https://img.shields.io/badge/release-v0.0.1-blue" />
  </a>
	<a  href="https://github.com/Wordcab/wordcab-transcribe/actions?workflow=Quality Checks" target="_blank">
		<img src="https://github.com/Wordcab/wordcab-transcribe/workflows/Quality Checks/badge.svg" />
	</a>
</div>


---

Describe the project.


> If you want to see...

## Key features

- ⚡ Fast: X.
- 🐳 Easy to deploy: X.
- 🔥 Batch requests: X.
- 💸 Cost-effective: X.
- 🫶 Easy-to-use API: X.
- 🤗 MIT License: X.
 
## Requirements

### Local development

- Linux _(tested on Ubuntu Server 20.04/22.04)_
- Python >=3.10, <3.12

#### Run the API locally 🚀

```bash
X
```

### Deployment

- [Docker](https://docs.docker.com/engine/install/ubuntu/) _(optional for deployment)_
- NVIDIA GPU + [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) _(optional for deployment)_

#### Run the API using Docker

Build the image.

```bash
docker build -t my-project:latest .
```

Run the container.

```bash
docker run -d --name wordcab-transcribe \
    --gpus all \
    --shm-size 1g \
    --restart unless-stopped \
    -p 5001:5001 \
    -v ~/.cache:/root/.cache \
    my-project:latest
```

### Run the API behind a reverse proxy

You can run the API behind a reverse proxy like Nginx. We have included a `nginx.conf` file to help you get started.

```bash
# Create a docker network and connect the api container to it
docker network create example-network
docker network connect example-network my-project

# Replace /absolute/path/to/nginx.conf with the absolute path to the nginx.conf
# file on your machine (e.g. /home/user/wordcab-transcribe/nginx.conf).
docker run -d \
    --name nginx \
    --network transcribe \
    -p 80:80 \
    -v /absolute/path/to/nginx.conf:/etc/nginx/nginx.conf:ro \
    nginx

# Check everything is working as expected
docker logs nginx
```

---

<details open>
<summary>⏱️ Profile the API</summary>

You can profile the process executions using `py-spy` as a profiler.

```bash
# Launch the container with the cap-add=SYS_PTRACE option
docker run -d --name my-project \
    --gpus all \
    --shm-size 1g \
    --restart unless-stopped \
    --cap-add=SYS_PTRACE \
    -p 5001:5001 \
    -v ~/.cache:/root/.cache \
    my-project:latest

# Enter the container
docker exec -it my-project /bin/bash

# Install py-spy
pip install py-spy

# Find the PID of the process to profile
top  # 28 for example

# Run the profiler
py-spy record --pid 28 --format speedscope -o profile.speedscope.json

# Launch any task on the API to generate some profiling data

# Exit the container and copy the generated file to your local machine
exit
docker cp my-project:/app/profile.speedscope.json profile.speedscope.json

# Go to https://www.speedscope.app/ and upload the file to visualize the profile
```

</details>

---

## Test the API

X.

## 🚀 Contributing

### Getting started

1. Before you start:

```bash
```

2. Clone the repo

```bash
git clone
cd my-project
```

3. Install dependencies and start coding

```bash
pip install -r requirements.txt
```

4. Run tests

```bash
```

### Working workflow

1. Create an issue for the feature or bug you want to work on.
2. Create a branch using the left panel on GitHub.
3. `git fetch`and `git checkout` the branch.
4. Make changes and commit.
5. Push the branch to GitHub.
6. Create a pull request and ask for review.
7. Merge the pull request when it's approved and CI passes.
8. Delete the branch.
9. Update your local repo with `git fetch` and `git pull`.
