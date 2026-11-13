// CYPHER CI/CD pipeline
// Jenkins job type: "Pipeline" -> "Pipeline script from SCM", branch */main,
// with "GitHub hook trigger for GITScm polling" enabled.
//
// Jenkins credentials used (Manage Jenkins -> Credentials):
//   aws-account-id   (Secret text)  your 12-digit AWS account ID
// AWS access comes from the EC2 instance's IAM role — no access keys are stored anywhere.

pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '15'))
        timeout(time: 30, unit: 'MINUTES')
    }

    triggers {
        githubPush()
    }

    environment {
        AWS_REGION   = 'ap-south-1'        // change if your resources are in another region
        ECR_REPO     = 'cypher'
        APP_DIR      = 'cypher'
        // Fill in after Task 5 to invalidate the CDN cache on every deploy (leave '' to skip)
        CLOUDFRONT_DISTRIBUTION_ID = ''
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_SHORT = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_SHORT}"
                }
                echo "Building version ${env.IMAGE_TAG}"
            }
        }

        stage('Install') {
            steps {
                dir(env.APP_DIR) {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install -q --upgrade pip
                        pip install -q -r requirements-dev.txt
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                dir(env.APP_DIR) {
                    sh '. .venv/bin/activate && python -m pytest -v --junitxml=test-results.xml'
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: "${env.APP_DIR}/test-results.xml"
                }
            }
        }

        stage('Build') {
            steps {
                dir(env.APP_DIR) {
                    // Byte-compile the app and confirm the ML model loads; fails the build on any error
                    sh '''
                        . .venv/bin/activate
                        python -m compileall -q app.py src
                        python -c "import joblib; joblib.load('model/phishing_model.pkl'); print('model OK')"
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${ECR_REPO}:${IMAGE_TAG} .'
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
                    sh '''
                        REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                        aws ecr get-login-password --region "$AWS_REGION" \
                          | docker login --username AWS --password-stdin "$REGISTRY"
                        docker tag "${ECR_REPO}:${IMAGE_TAG}" "$REGISTRY/${ECR_REPO}:${IMAGE_TAG}"
                        docker tag "${ECR_REPO}:${IMAGE_TAG}" "$REGISTRY/${ECR_REPO}:latest"
                        docker push "$REGISTRY/${ECR_REPO}:${IMAGE_TAG}"
                        docker push "$REGISTRY/${ECR_REPO}:latest"
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
                    // deploy.sh runs a health check and automatically rolls back if the new version fails
                    sh '''
                        REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                        bash deploy/deploy.sh "$REGISTRY/${ECR_REPO}:${IMAGE_TAG}"
                    '''
                }
            }
        }

        stage('Invalidate CDN') {
            when { expression { return env.CLOUDFRONT_DISTRIBUTION_ID?.trim() } }
            steps {
                sh '''
                    aws cloudfront create-invalidation \
                      --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" \
                      --paths "/*"
                '''
            }
        }
    }

    post {
        success {
            echo "Deployed ${env.IMAGE_TAG} successfully"
        }
        failure {
            echo 'Pipeline failed — the previously running version was left in place.'
        }
        always {
            // Remove dangling layers so the disk doesn't fill up
            sh 'docker image prune -f || true'
        }
    }
}
