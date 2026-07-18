from pypureclient import flasharray
from pypureclient import responses
from pypureclient.flasharray import Client as FAClient

#---------------------FA Tools Start-------------------------

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