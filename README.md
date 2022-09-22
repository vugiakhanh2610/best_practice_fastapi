# Environment Setup
conda create -n bp_fastapi python=3.9
conda activate bp_fastapi
pip install -r requirements.txt 

# Run docker
cd docker
docker-compose up

# Database Setup
create database demo

# Run project
sh bin/run.sh
