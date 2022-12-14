# julieops-jenkins-pipeline-library
A central shared pipeline for automating JulieOps on Jenkins!! NICE!! Primarily used in a Jenkinsfile for creating the julieOps template.

Templating logics works with one or multiple prefixes 


## Usage
```shell
$ python3 julieops_config_generator.py --mds-url test --mds-username sion --mds-password password --kafka-cluster-id abc --schema-registry-url https://localhost:8081 --tenant-state-topic _julieops_test --managed-topics-list test1 test2
```

### Sample output with multiple prefixes
```shell
sasl.mechanism=OAUTHBEARER
security.protocol=SASL_PLAINTEXT
sasl.jaas.config=org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required username="sion" password="password" metadataServerUrls="test";
sasl.login.callback.handler.class=io.confluent.kafka.clients.plugins.auth.token.TokenUserLoginCallbackHandler
topology.builder.access.control.class=com.purbon.kafka.topology.roles.RBACProvider
topology.builder.mds.server=test
topology.builder.mds.user=sion
topology.builder.mds.password=password
topology.builder.mds.kafka.cluster.id=abc
schema.registry.url=https://localhost:8081
schema.registry.basic.auth.user.info=sion:password
basic.auth.credentials.source=USER_INFO
topology.builder.mds.schema.registry.cluster.id=schema-registry
topology.builder.mds.kafka.connect.cluster.id=connect-cluster
topology.builder.mds.ksqldb.cluster.id=ksql-cluster
topology.topic.prefix.separator=-
topology.project.prefix.format=
topology.topic.prefix.format={{context}}-{{topic}}
julie.instance.id=julieops_
julie.kafka.config.topic=_julieops_test
topology.builder.state.processor.class=com.purbon.kafka.topology.backend.KafkaBackend
allow.delete.topics=true
julie.multiple.context.per.dir.enabled=true
topology.topic.managed.prefixes.0=test1
topology.topic.managed.prefixes.1=test2
julie.verify.remote.state=true
julie.roles=custom-roles/role-bindings.yaml
allow.delete.bindings=true
```