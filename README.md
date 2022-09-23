# Environment Setup
conda create -n bp_fastapi python=3.9
conda activate bp_fastapi
pip install -r requirements.txt 

# Setup pre-commit
put 'pre-commit' in requirements.txt 
pip install -r requirements.txt 
pre-commit install
create and config file .pre-commit-config.yaml

# Run docker
cd docker
docker-compose up

# Database Setup
create database demo

# Run project
sh bin/run.sh
