pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "todoproject:${BUILD_NUMBER}"
        REGISTRY = "docker.io"  // Change to your Docker registry
        REGISTRY_CREDENTIALS = "docker-credentials"  // Jenkins credentials ID
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                script {
                    sh '''
                        docker-compose -f docker-compose.yml up -d
                        docker-compose exec -T web python manage.py test
                        docker-compose down
                    '''
                }
            }
        }

        stage('Run Migrations') {
            steps {
                echo 'Running database migrations...'
                script {
                    sh '''
                        docker-compose -f docker-compose.yml up -d
                        docker-compose exec -T web python manage.py migrate
                        docker-compose down
                    '''
                }
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Running code quality checks...'
                script {
                    sh '''
                        docker run --rm ${DOCKER_IMAGE} bash -c "pip install flake8 && flake8 . --max-line-length=100 --exclude=migrations,venv"
                    '''
                }
            }
        }

        stage('Push to Registry') {
            when {
                branch 'main'  // Only push on main branch
            }
            steps {
                echo 'Pushing image to registry...'
                script {
                    withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin ${REGISTRY}
                            docker tag ${DOCKER_IMAGE} ${REGISTRY}/todoproject:latest
                            docker push ${REGISTRY}/todoproject:latest
                            docker logout ${REGISTRY}
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'  // Only deploy on main branch
            }
            steps {
                echo 'Deploying application...'
                script {
                    sh '''
                        docker-compose down
                        docker-compose up -d
                        echo "Application deployed successfully"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker resources...'
            sh 'docker-compose down || true'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
