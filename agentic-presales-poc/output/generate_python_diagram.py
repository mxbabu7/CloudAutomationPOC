from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import SQS
from diagrams.aws.analytics import Glue
from diagrams.aws.database import RDS
from diagrams.aws.security import KMS
from diagrams.aws.devtools import CodePipeline

with Diagram("AWS Architecture Diagram", show=False, filename="output_architecture"):
    with Cluster("Presentation Layer"):
        web_ui = EC2("Web UI")
        mobile_app = EC2("Mobile App")

    with Cluster("Application Layer"):
        api_gateway = APIGateway("API Gateway")
        microservices = EC2("Microservices")
        ci_cd_pipeline = CodePipeline("CI/CD Pipeline")

    with Cluster("Data Layer"):
        databricks = Glue("Databricks")
        db2_migration = EC2("DB2 Migration Service")
        data_lake = RDS("Data Lake")

    with Cluster("Integration Layer"):
        message_queue = SQS("Message Queue")
        event_streaming = EC2("Event Streaming")

    with Cluster("Security Layer"):
        tokenization_service = KMS("Tokenization Service")
        encryption_service = KMS("Encryption Service")

    web_ui >> Edge(label="HTTPS") >> api_gateway
    api_gateway >> Edge(label="HTTPS") >> microservices
    microservices >> Edge(label="HTTPS") >> databricks
    databricks >> Edge(label="HTTPS") >> data_lake
    microservices >> Edge(label="HTTPS") >> tokenization_service