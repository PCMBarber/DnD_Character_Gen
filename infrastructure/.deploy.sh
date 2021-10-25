#!/bin/bash
terraform init
terraform apply -auto-approve
git add . 
git commit -m "deploying"
git push