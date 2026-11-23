pipeline {
    agent any
    options {
        skipDefaultCheckout()
        disableConcurrentBuilds()
        timestamps()
    }
    triggers { githubPush() }
    environment {
        APP_IMAGE = "cicd-assignment-fa23-bct-039:${BUILD_NUMBER}"
        TEST_IMAGE = 'cicd-assignment-fa23-bct-039-test:local'
        STAGING = "cicd-fa23-bct-039-stage-${BUILD_NUMBER}"
        NETWORK = "cicd-fa23-bct-039-net-${BUILD_NUMBER}"
        LIVE = 'cicd-fa23-bct-039-live'
        LIVE_PORT = '8091'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Package') {
            steps { sh 'docker build -t "$APP_IMAGE" .' }
        }
        stage('Start Staging') {
            steps {
                sh '''
                    docker network create "$NETWORK"
                    docker run -d --name "$STAGING" --network "$NETWORK" "$APP_IMAGE"
                    timeout 30 sh -c 'until docker exec "$STAGING" wget -q -O /dev/null http://127.0.0.1; do sleep 1; done'
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    rm -f reports/junit.xml reports/selenium-text-submit.png
                    mkdir -p reports
                    docker build -f test.Dockerfile -t "$TEST_IMAGE" .
                    docker run --rm --network "$NETWORK" --user "$(id -u):$(id -g)" \
                        -e HOME=/tmp -e APP_URL="http://$STAGING" \
                        -v "$PWD:/workspace" "$TEST_IMAGE" \
                        pytest -p no:cacheprovider -v --junitxml=reports/junit.xml tests
                '''
            }
            post {
                always {
                    junit 'reports/junit.xml'
                    archiveArtifacts artifacts: 'reports/*.png', allowEmptyArchive: true
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    if docker container inspect "$LIVE" >/dev/null 2>&1; then
                        docker rm -f "$LIVE"
                    fi
                    docker run -d --restart unless-stopped --name "$LIVE" \
                        -p "127.0.0.1:$LIVE_PORT:80" "$APP_IMAGE"
                    curl --fail --silent --show-error --retry 5 --retry-connrefused \
                        "http://127.0.0.1:$LIVE_PORT/" -o /dev/null
                '''
            }
        }
    }
    post {
        always {
            sh '''
                docker rm -f "$STAGING" >/dev/null 2>&1 || true
                docker network rm "$NETWORK" >/dev/null 2>&1 || true
            '''
        }
    }
}
