"""
This module returns a AML workspace object after authentication.

Args:
--subscription_id: The Azure subscription ID.
This argument is required for identifying the Azure subscription.
--resource_group_name: The name of the resource group associated with
AML workspace.
--workspace_name: The AML workspace name.
"""
from azure.ai.ml.dsl import pipeline
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml import command
from azure.ai.ml import Input, Output
from azure.ai.ml import Input, Output
from azure.ai.ml.entities import Data
from azure.ai.ml import MLClient
from azure.ai.ml.constants import AssetTypes
import os
import argparse
import json

pipeline_components = []

def get_aml_client(
        subscription_id,
        resource_group_name,
        workspace_name,
):
    aml_client = MLClient(
        DefaultAzureCredential(),
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
    )

    return aml_client

def register_data_asset(
        name,
        description,
        target_dir,
        aml_client,
        sa_account_name,
        sa_container_name
):

    target_path = f"https://{sa_account_name}.blob.core.windows.net/{sa_container_name}/{target_dir}"
    aml_dataset = Data(
        path = target_path,
        type = AssetTypes.URI_FILE,
        description = description,
        name = name
    )

    aml_client.data.create_or_update(aml_dataset)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subscription_id",
        type=str,
        help="Azure subscription id",
        required=True,
    )
    parser.add_argument(
        "--resource_group_name",
        type=str,
        help="Azure resource group",
        required=True,
    )
    parser.add_argument(
        "--workspace_name",
        type=str,
        help="Azure ML workspace",
        required=True,
    )
    parser.add_argument(
        "--sa_account_name",
        type=str,
        help="Storage account name",
        required=True,
    )

    parser.add_argument(
        "--sa_container_name",
        type=str,
        help="Storage account's container name",
        required=True,
    )

    parser.add_argument(
        "--config_path_root_dir",
        type=str,
        help="Root dir for config file",
        required=True,
    )

    args = parser.parse_args()

    subscription_id = args.subscription_id
    resource_group_name = args.resource_group_name
    workspace_name = args.workspace_name
    config_path_root_dir = args.config_path_root_dir
    sa_account_name = args.sa_account_name
    sa_container_name = args.sa_container_name

    config_path = os.path.join(os.getcwd(), f"{config_path_root_dir}/configs/dataops_config.json")
    config = json.load(open(config_path))

    aml_client = get_aml_client(
        subscription_id,
        resource_group_name,
        workspace_name,
    )

    data_asset_configs = config['DATA_ASSETS']
    for data_asset_config in data_asset_configs:
        data_asset_name = data_asset_config['NAME']
        data_asset_file_path = data_asset_config['PATH']
        data_asset_description = data_asset_config['DESCRIPTION']

        register_data_asset(
            name = data_asset_name,
            description = data_asset_description,
            target_dir = data_asset_file_path,
            aml_client = aml_client,
            sa_account_name=sa_account_name,
            sa_container_name=sa_container_name
        )

if __name__ == "__main__":
    main()