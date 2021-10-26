resource "local_file" "tf_docker_compose" {
  content = <<-DOC
version: '3.7'
services:
    nginx:
      image: nginx:latest
      ports:
        - target: 80
          published: 80
          protocol: tcp
      volumes:
        - type: bind
          source: ./nginx/nginx.conf
          target: /etc/nginx/nginx.conf
      depends_on:
        - frontend

    frontend:
      image: ${var.docker_user}/frontend:build-0
      build: ./frontend
      ports:
        - target: 5000
          published: 5000
    
    service1:
      image: ${var.docker_user}/rand1:build-0
      build: ./randapp1
      ports:
        - target: 5001
          published: 5001
      
    service2:
      image: ${var.docker_user}/rand2:build-0
      build: ./randapp2
      ports:
        - target: 5002
          published: 5002

    backend:
      image: ${var.docker_user}/backend:build-0
      build: ./backend
      ports:
        - target: 5003
          published: 5003

    DOC
  filename = "../docker-compose.yaml"
}
resource "local_file" "tf_ansible_inventory" {
  content = <<-DOC
    [jenkins]
    ${module.ec2.jenk_ip} ansible_ssh_private_key_file=~/.ssh/${var.key_name}.pem

    [jenkins:vars]
    ansible_user=ubuntu
    ansible_ssh_common_args='-o StrictHostKeyChecking=no'
    DOC
  filename = "./ansible/inventory"
}
resource "local_file" "tf_Jenkinsfile" {
  content = <<-DOC
    pipeline{
                agent any
                stages{
                        stage('--Front End--'){
                                steps{
                                        sh '''
                                                image="${var.docker_user}/frontend:build-$BUILD_NUMBER"
                                                docker build -t $image /var/lib/jenkins/workspace/$JOB_BASE_NAME/frontend
                                                docker push $image
                                                kubectl set image deployment/frontend frontend=$image
                                        '''
                                }
                        }  
                        stage('--Service1--'){
                                steps{
                                        sh '''
                                                image="${var.docker_user}/rand1:build-$BUILD_NUMBER"
                                                docker build -t $image /var/lib/jenkins/workspace/$JOB_BASE_NAME/randapp1
                                                docker push $image
                                                kubectl set image deployment/service1 service1=$image
                                        '''
                                }
                        }
                        stage('--Service2--'){
                                steps{
                                        sh '''
                                                image="${var.docker_user}/rand2:build-$BUILD_NUMBER"
                                                docker build -t $image /var/lib/jenkins/workspace/$JOB_BASE_NAME/randapp2
                                                docker push $image
                                                kubectl set image deployment/service2 service2=$image
                                        '''
                                }
                        }
                        stage('--Back End--'){
                                steps{
                                        sh '''
                                                image="${var.docker_user}/backend:build-$BUILD_NUMBER"
                                                docker build -t $image /var/lib/jenkins/workspace/$JOB_BASE_NAME/backend
                                                docker push $image
                                                kubectl set image deployment/backend backend=$image
                                        '''
                                }
                        }
                }
        }
    DOC
  filename = "../Jenkinsfile"
}

resource "local_file" "tf_InsecureRegistry" {
  content = <<-DOC
{
        "insecure-registries":["${module.ec2.jenk_ip}:5000"]
}
    DOC
  filename = "./daemon.json"
}

resource "local_file" "tf_frontend_yaml" {
  content = <<-DOC
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: ClusterIP
  selector:
    app: frontend
  ports:
  - name: flask
    port: 5000
    targetPort: 5000
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  selector:
    matchLabels:
      app: frontend
  replicas: 3
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: ${var.docker_user}/frontend:build-0
        ports:
          - containerPort: 5000
        env:
        - name: MYSQL_USER
          valueFrom:
            secretKeyRef:
              name: credentials
              key: MYSQL_USER
        - name: MYSQL_PWD
          valueFrom:
            secretKeyRef:
              name: credentials
              key: MYSQL_PWD
        - name: MYSQL_IP
          valueFrom:
            secretKeyRef:
              name: credentials
              key: MYSQL_IP
        - name: MYSQL_DB
          valueFrom:
            secretKeyRef:
              name: credentials
              key: MYSQL_DB
        - name: MYSQL_SK
          valueFrom:
            secretKeyRef:
              name: credentials
              key: MYSQL_SK
    DOC
  filename = "../kubernetes/frontend.yaml"
}

resource "local_file" "tf_backend_yaml" {
  content = <<-DOC
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - name: flask
    port: 5003
    targetPort: 5003
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  labels:
    app: backend
spec:
  selector:
    matchLabels:
      app: backend
  replicas: 3
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: ${var.docker_user}/backend:build-0
        ports:
          - containerPort: 5003
    DOC
  filename = "../kubernetes/backend.yaml"
}

resource "local_file" "tf_randapp1_yaml" {
  content = <<-DOC
apiVersion: v1
kind: Service
metadata:
  name: service1
spec:
  type: ClusterIP
  selector:
    app: service1
  ports:
  - name: flask
    port: 5001
    targetPort: 5001
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service1
  labels:
    app: service1
spec:
  selector:
    matchLabels:
      app: service1
  replicas: 3
  template:
    metadata:
      labels:
        app: service1
    spec:
      containers:
      - name: service1
        image: ${var.docker_user}/rand1:build-0
        ports:
          - containerPort: 5001
    DOC
  filename = "../kubernetes/randapp1.yaml"
}

resource "local_file" "tf_randapp2_yaml" {
  content = <<-DOC
apiVersion: v1
kind: Service
metadata:
  name: service2
spec:
  type: ClusterIP
  selector:
    app: service2
  ports:
  - name: flask
    port: 5002
    targetPort: 5002
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service2
  labels:
    app: service2
spec:
  selector:
    matchLabels:
      app: service2
  replicas: 3
  template:
    metadata:
      labels:
        app: service2
    spec:
      containers:
      - name: service2
        image: ${var.docker_user}/rand2:build-0
        ports:
          - containerPort: 5002
    DOC
  filename = "../kubernetes/randapp2.yaml"
}