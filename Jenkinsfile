pipeline {
    agent any
    stages {
        stage('Clone Code') {
            steps {
                // IMPORTANT: Replace this with your actual GitHub repo URL
                git branch: 'main', url: 'https://github.com/heetpatel28/flask-app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-app:latest .'
            }
        }
        stage('Deploy with Docker Compose') {
            steps {
                // Stop any running containers from a previous build
                sh 'docker compose down || true' 
                // Start new containers, --build forces a rebuild of the flask image
                sh 'docker compose up -d --build'
            }
        }
    }
}