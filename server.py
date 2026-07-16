from fastmcp import FastMCP
import fatools
import json

mcp = FastMCP("famcp")

#load array info which saved in a local JSON file named fainfo.json.
with open("fainfo.json","r") as jfile:
  array_info : list = json.load(jfile)

print(array_info)

#check if array infor is predefined in config file(fainfo.json).
def check_array_info(array_name:str) -> dict:
  current_array:dict = {
    "array_name":"",
    "api_token":""
  }
  
  for i in array_info:
    if i["array_name"] == array_name:
      current_array["array_name"] = i["array_name"]
      current_array["api_token"] = i["api_token"]
  
  return current_array


#tool for crate a volume
@mcp.tool()
def Create_Volume(array_name:str, volume_name:str, volume_size:int) -> str:
  """
    Create a storage volume on a specific Everpure FlashArray.

    Args:
      array_name: The IP address or FQDN of the management port of the specific Everpure FlashArray.
      volume_name: The name of the volume.
      volume_size: The size of the volume. The unit is GB.

    Returns:
      Results of the job. 
  """
  current_array = check_array_info(array_name)
  
  if current_array["array_name"] == "":
    return "ERROR: Array not found in config file. Please add it first!"

  current_client = fatools.Create_FA_Client(current_array)
  results = fatools.Create_One_Volume(current_client,volume_name, volume_size)
  
  return results

@mcp.tool()
def Create_Host(array_name:str, host_name:str, protocol_type:str, endpoint_ids:list[str], personality:str = "") -> str:
  """
    Create a host on a given Everpure FlashArray

    Args:
      array_name: The IP address or FQDN of the management port of the specific Everpure FlashArray.
      host_name: The name of the host to be created on the array.
      protocol_type: The protocol to be used to connect host and the array. Should be one of fc/iscsi/nvme.
      endpoint_ids: The protocol related IDs. WWN for fc, IQN for iscsi, NQN for nvme.
      personality: Determines how the system tunes the array to ensure that it works optimally with the host. Set personality to the name of the host operating system or virtual memory system. Valid values are aix, esxi, hitachi-vsp, hpux, oracle-vm-server, solaris, vms, nutanix-mgmt and nutanix-cluster. If your system is not listed as one of the valid host personalities, do not set the option. By default, the personality is not set.

    Returns:
      Results of the job.
  """

  # Check if the given array name is in the configuration file
  current_array = check_array_info(array_name)
  if current_array["array_name"] == "":
    return "ERROR: Array not found in config file. Please add it first!"

  current_client = fatools.Create_FA_Client(current_array)
  results = fatools.Create_One_Host(current_client,host_name,protocol_type,endpoint_ids,personality)
  
  return results

@mcp.tool()
def Connect_Volume(array_name:str, host_group_name:bool=False,host_name:str="", volume_name:str="" ) -> str:
  """
    Connect a given volume to a host on a specific Everpure FlashArray.

    Args:
      array_name: The IP address or FQDN of the management port of the specific Everpure FlashArray.
      host_name: The name of the host which was defined on the given Everpure FlashArray and will connect to the given volume. This is a optional parameter.
      host_group: Set to True if the host_name refers to a host group name. Set to False if it's not. Default value is False.
      volume_name: The name of the volume which was created before and will be connected to the given host or host group.

    Returns:
      Results of the job.
  """
  # Check if the given array name is in the configuration file
  current_array = check_array_info(array_name)
  if current_array["array_name"] == "":
    return "ERROR: Array not found in config file. Please add it first!"

  current_client = fatools.Create_FA_Client(current_array)
  results = fatools.Connect_One_Volume(current_client,host_group,host_name,volume_name)

  return results

@mcp.tool()
def Create_Snapshot(array_name:str, volume_name:str="", snapshot_name:str="") -> str:
  # under construction
  """
    Create a snapshot from given storage volume on given Everpure FlashArray.

    Args:
      array name: The IP address or FQDN of the management port of the specific Everpure FlashArray.
      volume name: The name of the volume which snapshot will be created from.
      snapshot name: The name of the snapshot.

    Returns:
      The results of the job.
  """

  results = f"The snapshot {snapshot_name} has been created on {storage_name}."

  return results

if __name__ == "__main__":
  mcp.run(transport="streamable-http", host="0.0.0.0", port=8765)
