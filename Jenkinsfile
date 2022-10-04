def confirmDeployment

final KAFKA_ADMIN_TEMPLATE = '''
sasl.mechanism=OAUTHBEARER
security.protocol=SASL_PLAINTEXT
sasl.jaas.config=org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required username="${MDS_USERNAME}" password="${MDS_PASSWORD}" metadataServerUrls="${MDS_URL}";
sasl.login.callback.handler.class=io.confluent.kafka.clients.plugins.auth.token.TokenUserLoginCallbackHandler
topology.builder.access.control.class=com.purbon.kafka.topology.roles.RBACProvider
topology.builder.mds.server=$(MDS_URL}
topology.builder.mds.user=${MDS_USERNAME}
topology.builder.mds.password=${MDS_PASSWORD}
topology.builder.mds.kafka.cluster.id=${KAFKA_CLUSER_ID}
schema.registry.url=${SCHEMA_REGISTRY_URL}
schema.registry.basic.auth.user.info=${MDS_USERNAME}:${MDS_PASSWORD}
basic.auth.credentials.source=USER_INFO
topology.builder.mds.schema.registry.cluster.id=schema-registry
topology.builder.mds.kafka.connect.cluster.id=connect-cluster
topology.builder.mds.ksqldb.cluster.id=ksql-cluster
topology.topic.prefix.separator=-
'''

def renderTemplate(template, bindings) {
    bindings.inject(template) { t, k, v -> t.replace("\${" + k + "}", v) }
}

pipeline {
    agent any
    options {
        disableConcurrentBuilds()
    }
    environment {
        env = "BLD"
        TopologyFiles = "topologies/descriptor.yaml"
        Brokers = "broker:10091"
        MDS_URL = "http://broker:8091"
        MDS_USERNAME = "mds"
        MDS_PASSWORD = "mds"
        KAFKA_CLUSER_ID = "6_bXN6WTQFaaMoIjWmh2UA"
        SCHEMA_REGISTRY_URL = "http://schema-registry:8081"
        ALLOW_TOPIC_DELETE = true
    }
    stages {
//        stage('check out schemas') {
//            steps {
//                sh 'git clone --branch main https://github.com/sionsmith/demo-platform-kafka-schemas.git '
//            }
//
//        }
        stage('verify-replication-factor') {
            steps {
                sh '''#!/bin/bash
                        verify-replication-factor(){
                            FILE=$1
                            REQUIRED_FACTOR=$2
                            required=`cat $FILE | grep replication.factor | wc -l`
                            matches=`cat $FILE | grep replication.factor | grep $REQUIRED_FACTOR | wc -l`
                        
                            if [ "$matches" -ne "$required" ] ;
                            then
                               echo -e "Some topics have not the expected replication factor, please review"
                               exit 1
                            elif [ "$matches" -eq "$required" ]  ;
                            then
                               echo -e "All topics have the required replication factor"
                               exit 0
                            fi
                        }
                        verify-replication-factor ${TopologyFiles} 1
                '''
            }
        }
        stage('verify-num-of-partitions') {
            steps {
                sh '''#!/bin/bash
                        verify-num-of-partitions(){
                            FILE=$1
                            REQUIRED_FACTOR=$2
                            
                            required=`cat $FILE | grep num.partitions | wc -l`
                            matches=`cat $FILE | grep num.partitions | grep $REQUIRED_FACTOR | wc -l`
                            
                            if [ "$matches" -ne "$required" ] ;
                            then
                               echo -e "Some topics have not the expected num of partitions, please review"
                               exit 1
                            elif [ "$matches" -eq "$required" ]  ;
                            then
                               echo -e "All topics have the required num of partitions"
                               exit 0
                            fi
                        }
                        verify-num-of-partitions ${TopologyFiles} 1
                '''
            }
        }
        stage('validate-role-bindings') {
            steps {
                sh '''#!/bin/bash
                        validate-role-bindings(){
                            FILE=$1
                            
                            resourceOwner=`cat $FILE | grep ResourceOwner | wc -l`
                            securityAdmin=`cat $FILE | grep SecurityAdmin | wc -l`
                        }
                        validate-role-bindings ${TopologyFiles}
                '''
            }
        }

        stage('dry-run') {
            steps {
                writeFile file: 'topology-builder.properties', text: renderTemplate(KAFKA_ADMIN_TEMPLATE, [
                        'MDS_USERNAME': env.MDS_USERNAME,
                        'MDS_PASSWORD': env.MDS_PASSWORD,
                        'MDS_URL': env.MDS_URL,
                        'KAFKA_CLUSER_ID': env.KAFKA_CLUSER_ID,
                        'SCHEMA_REGISTRY_URL': env.SCHEMA_REGISTRY_URL]
                )
                sh 'java -jar /app/julie-ops.jar --brokers ${Brokers} --clientConfig topology-builder.properties --topology ${TopologyFiles} --dryRun'
            }
        }
        stage('Confirm Topology') {
            when {
                branch 'int'
            }
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    script {
                        confirmDeployment = input(id: 'userInput', message: 'Apply changes?',
                                parameters: [[$class     : 'ChoiceParameterDefinition', defaultValue: 'strDef',
                                              description: 'describing choices', name: 'DeploymentChoice', choices: "yes\nno"]
                                ])

                        if (confirmDeployment == 'no') {
                            currentBuild.result = 'ABORTED'
                            error("Aborted by user")
                        }
                    }
                }
            }
        }
        stage('run') {
            steps {
                sh './scripts/build-connection-file.sh > topology-builder.properties'
                sh 'cat topology-builder.properties'
                sh 'java -jar /app/julie-ops.jar --brokers ${Brokers} --clientConfig topology-builder.properties --topology ${TopologyFiles}'
            }
        }
    }
}
