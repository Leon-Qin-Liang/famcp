import json
from pypureclient import flasharray
from pypureclient import responses
from pypureclient.flasharray import Client as FAClient

#---------------------FA Tools For Operating Start-------------------------

# Create FlashArray Client
def Create_FA_Client(array_info:dict) -> FAClient:
    try:
        fa_client = FAClient(array_info["array_name"], api_token=array_info["api_token"])
        return fa_client
    except Exception as e:
        return e

# Create a single volume on given FlashArray
def Create_One_Volume(fa_client:FAClient,volume_name:str,volume_size:int) -> str:

    #create VolumePost Object with required volume size which is in Byte.   
    vol_post = flasharray.VolumePost(provisioned=volume_size*1024*1024*1024)
    #create volume with given parameters.
    client_response = fa_client.post_volumes(vol_post,names=[volume_name],with_default_protection=False)
    if type(client_response) is responses.ErrorResponse:
        return "ERROR:" + client_response.errors[0].message

    return f"Volume {volume_name} created."

# Create a single host on given FlashArray
def Create_One_Host(fa_client:FAClient, host_name:str, protocol_type:str, host_wwn:list[str], personality:str) -> str:

    if protocol_type == "fc":
        host_post = flasharray.HostPost(wwns=host_wwn,personality=personality)
    elif protocol_type == "iscsi":
        host_post = flasharray.HostPost(iqns=host_wwn,personality=personality)
    elif protocol_type == "nvme":
        host_post = flasharray.HostPost(nqns=host_wwn,personality=personality)
    else:
        return f"ERROR: {protocol_type} not supported. Please specify a supported protocol."
    
    client_response = fa_client.post_hosts(host_post,names=[host_name])
    if type(client_response) is responses.ErrorResponse:
        return "ERROR:" + client_response.errors[0].message
    
    return f"Host {host_name} created."

# Create a host group
def Create_Host_Group(fa_client:FAClient, host_group_name:str) -> str:
    client_response = fa_client.post_host_groups(names=[host_group_name])
    if type(client_response) is responses.ErrorResponse:
        return "ERROR:" + client_response.errors[0].message
    
    return f"Host group {host_group_name} created."

# Add host to host group
def Add_Host_To_Host_Group(fa_client:FAClient, host_name:str, host_group_name:str) -> str:
    client_response = fa_client.post_host_groups_hosts(group_names=[host_group_name], member_name=[host_name])
    if type(client_response) is responses.ErrorResponse:
        return "ERROR:" + client_response.errors[0].message
    
    return f"Host {host_name} has been added to host group {host_group_name}"

# Connect a volume to a host
def Connect_Volume_To_Host(fa_client:FAClient,host_name:str,volume_name:str) -> str:
    client_response = fa_client.post_connections(host_names=[host_name],volume_names=[volume_name])
    if type(client_response) is responses.ErrorResponse:
        return "ERROR:" + client_response.errors[0].message
    else:
        return f"Volume {volume_name} has been connected to host {host_name}."

# Create a volume snapshot
def Create_Volume_Snapshot(fa_client:FAClient,volume_name:str,snapshot_name:str) -> str:
    volume_snapshot_post = flasharray.VolumeSnapshotPost(suffix=snapshot_name)

    client_response = fa_client.post_volume_snapshots(volume_snapshot_post,source_names=[volume_name])
    if type(client_response) is responses.ErrorResponse:
        return "ERROR:" + client_response.errors[0].message
    else:
        return f"Snapshot {snapshot_name} from volume {volume_name} has been created."

#---------------------FA Tools For Operating End-------------------------


#---------------------FA Tools For Getting Information Start-------------------------

# Get all volumes information of a given Everpure FlashArray
def Get_Volumes(fa_client:FAClient) -> json:
    readable_result:list = []

    client_response:responses = fa_client.get_volumes()
    if type(client_response) is responses.ErrorResponse:
        return "ERROR:" + client_response.errors[0].message
    else:
        results = client_response.to_dict()
        items:list = results["items"]
        
        for item in items:
            current_dict:dict = {}
            current_dict["name"] = item["name"]
            current_dict["provisioned"] = item["provisioned"]
            current_dict["qos"] = item["qos"]
            current_dict["serial"] = item["serial"]
            current_dict["data_reduction"] = item["space"]["data_reduction"]
            current_dict["used_space"] = item["space"]["virtual"]
            current_dict["pod"] = item["pod"]
            current_dict["volume_group"] = item["volume_group"]
            readable_result.append(current_dict)
        
        return json.dumps(readable_result)
