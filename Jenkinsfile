pipeline {
    agent any

    environment {
        // Optional: define app name and tag
        IMAGE_NAME = 'flask-app'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Clone Code') {
            steps {
                echo 'Cloning the repository...'
                git branch: 'main', url: 'https://github.com/heetpatel28/flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo 'Deploying with Docker Compose...'
                sh '''
                    # Stop previous containers if any
                    docker compose down || true

                    # Start containers in detached mode and rebuild if needed
                    docker compose up -d --build
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment completed successfully!'
        }
        failure {
            echo '❌ Build or deployment failed. Check logs above.'
        }
    }
}
