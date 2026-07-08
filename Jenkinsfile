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
                sh 'docker rm -f linux-monitor-container || true'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                --name linux-monitor-container \
                -p 8080:80 \
                -v /:/host:ro \
                -v /var/run/docker.sock:/var/run/docker.sock \
                linux-monitor
                '''
            }
        }
    }
}
