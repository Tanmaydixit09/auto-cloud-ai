
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        IMAGE_NAME = 'autocloud-ai'
        IMAGE_TAG = 'jenkins'
        PYTHON = 'python'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out Auto Cloud AI source code'
                checkout scm
                bat 'git log -1 --oneline'
            }
        }

        stage('Python Environment') {
            steps {
                bat '''
                    python --version
                    python -m venv .venv-ci
                    .venv-ci\\Scripts\\python.exe -m pip install --upgrade pip
                    .venv-ci\\Scripts\\python.exe -m pip install -r requirements.txt
                    .venv-ci\\Scripts\\python.exe -m pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    .venv-ci\\Scripts\\python.exe -m pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit testResults: 'test-results.xml',
                          allowEmptyResults: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                bat '''
                    docker build -t autocloud-ai:jenkins .
                '''
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat '''
                    docker image inspect autocloud-ai:jenkins
                    docker images autocloud-ai
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Auto Cloud AI CI pipeline completed.'
        }
        failure {
            echo 'FAILED: Check the stage console output.'
        }
        always {
            echo 'Jenkins pipeline execution finished.'
        }
    }
}
