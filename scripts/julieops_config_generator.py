import os
import argparse
import jinja2

def generate_content():
    """
    Use jinja2 template to generate connector content
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
        KSQL_CLUSTER_ID=args.ksql_cluster_id
    )

    print(export)
    return export

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
    args = parser.parse_args()
    generate_content()