pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t linux-monitor .'
            }
        }

        stage('Remove Old Container') {
            steps {
                sh '''
                docker stop linux-monitor-container || true
                docker rm linux-monitor-container || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                --name linux-monitor-container \
                -p 8080:80 \
                linux-monitor
                '''
            }
        }
    }
}