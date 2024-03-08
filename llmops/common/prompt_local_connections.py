"""
This module evaluates bulk-runs using evaluation flows.

Args:
--subscription_id: The Azure subscription ID.
This argument is required for identifying the Azure subscription.
--build_id: The unique identifier for build execution.
This argument is required to identify the specific build execution.
--env_name: The environment name for execution/deployment.
This argument is required to specify the environment (dev, test, prod)
--data_purpose: The data identified by its purpose.
This argument is required to specify the purpose of the data.
--run_id: The bulk run IDs.
This argument is required to specify the bulk run IDs for execution.
--flow_to_execute: The name of the flow use case.
This argument is required to specify the name of the flow for execution.
"""

import argparse
import json
from promptflow.entities import AzureOpenAIConnection
from promptflow import PFClient

from llmops.common.logger import llmops_logger
from llmops.common.config_utils import LLMOpsConfig

logger = llmops_logger("prompt_aoai_connection")


def prepare_and_execute(
    flow_to_execute,
    stage,
    connection_details,
):
    """
    Run the evaluation loop by executing evaluation flows.

    reads latest evaluation data assets
    executes evaluation flow against each provided bulk-run
    executes the flow creating a new evaluation job
    saves the results in both csv and html format

    Returns:
        None
    """
    main_config = LLMOpsConfig(flow_name=flow_to_execute, environment=stage)
    model_config = main_config.model_config
    logger.info("valid environment is found")

    secret_config = json.loads(connection_details)

    pf = PFClient()

    webapp_endpoint_config = main_config.webapp_endpoint_config
    
    if "CONNECTION_NAMES" in elem and "ENV_NAME" in elem:
        if stage == elem["ENV_NAME"]:
            con_to_create = list(elem["CONNECTION_NAMES"])

            for con in con_to_create:
                for avail_con in secret_config:
                    if avail_con['name'] == con:
                        if avail_con['type'] == "azure_open_ai":
                            connection = AzureOpenAIConnection(
                                name=avail_con['name'],
                                api_key=avail_con['api_key'],
                                api_base=avail_con['api_base'],
                                api_type=avail_con['api_type'],
                                api_version=avail_con['api_version']
                            )
                            pf.connections.create_or_update(connection)

                            logger.info(
                                f"{avail_con['name']} created successfully"
                            )


def main():
    """
    Create local Azure OpenAI connection objects.

    Returns:
        None
    """
    parser = argparse.ArgumentParser("aoai_pf_connection")

    parser.add_argument(
        "--flow_to_execute",
        type=str,
        help="flow use case name",
        required=True
    )

    parser.add_argument(
        "--env_name",
        type=str,
        help="environment name(dev, test, prod) for execution and deployment",
        required=True,
    )

    parser.add_argument(
        "--connection_details",
        type=str,
        help="details of local pf connection name",
        required=True,
    )

    args = parser.parse_args()

    prepare_and_execute(
        args.flow_to_execute,
        args.env_name,
        args.connection_details
    )


if __name__ == "__main__":
    main()
