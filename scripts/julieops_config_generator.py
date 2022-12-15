import os
import argparse
import jinja2

def generate_content():
    """
    Use jinja2 template to generate topology content
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                             trim_blocks=True)
    config_template = env.get_template('topology.template')
    export = config_template.render(
        MDS_USERNAME=args.mds_username,
        MDS_PASSWORD=args.mds_password,
        MDS_URL=args.mds_url,
        KAFKA_CLUSER_ID=args.kafka_cluster_id,
        SCHEMA_REGISTRY_URL=args.schema_registry_url,
        SCHEMA_REGISTRY_ID=args.schema_registry_id,
        CONNECT_CLUSTER_ID=args.connect_cluster_id,
        KSQL_CLUSTER_ID=args.ksql_cluster_id,
        TENANT_STATE_TOPIC_NAME=args.tenant_state_topic,
        TOPIC_FORMAT=args.topic_format,
        MANAGED_PREFIXES=args.managed_topics_list,
        MANAGED_PREFIXES_LEN=len(args.managed_topics_list),
        ROLES_FILE=args.custom_roles_file
    )

    print(export)
    f = open("topology-builder.properties", "w")
    f.write(export)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--mds-url',
        type=str,
        required=True,
        help='Meta data service url',
    )
    parser.add_argument(
        '--mds-username',
        type=str,
        required=True,
        help='Meta data service username',
    )
    parser.add_argument(
        '--mds-password',
        type=str,
        required=True,
        help='Meta data service password',
    )
    parser.add_argument(
        '--kafka-cluster-id',
        type=str,
        required=True,
        help='Kafka cluster id',
    )
    parser.add_argument(
        '--schema-registry-url',
        type=str,
        required=True,
        help='Schema registry url',
    )
    parser.add_argument(
        '--schema-registry-id',
        type=str,
        default='schema-registry',
        help='Schema registry id',
    )
    parser.add_argument(
        '--connect-cluster-id',
        type=str,
        default='connect-cluster',
        help='Connect cluster id',
    )
    parser.add_argument(
        '--ksql-cluster-id',
        type=str,
        default='ksql-cluster',
        help='Ksql cluster id',
    )
    parser.add_argument(
        '--tenant-state-topic',
        type=str,
        required=True,
        help='Tenant state topic name',
    )
    parser.add_argument(
        '--managed-topics-list',
        nargs='+',
        required=True,
        default=[],
        help='List of topics for JulieOps to manage'
    )
    parser.add_argument(
        '--custom-roles-file',
        type=str,
        default='custom-roles/role-bindings.yaml',
        help='Filename of custom roles'
    )
    parser.add_argument(
        '--topic-format',
        type=str,
        default='{{context}}-{{topic}}',
        help='Format for topics names'
    )
    args = parser.parse_args()
    generate_content()