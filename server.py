from fastmcp import FastMCP
import fatools
import json

mcp = FastMCP("famcp")

#load array info which saved in a local JSON file named fainfo.json.
with open("fainfo.json","r") as jfile:
  array_info : dict = json.load(jfile)

print(array_info)

#check if array infor is predefined in config file(fainfo.json).
def Get_Array_Info(array_name:str) -> dict:
  current_array:dict = {
    "array_name":"",
    "api_token":""
  }
  
  for i in array_info["array_info"]:
    if i["array_name"] == array_name:
      current_array["array_name"] = i["array_name"]
      current_array["api_token"] = i["api_token"]
  
  return current_array

# tool for listing volume names
@mcp.tool()
def Get_Volumes(array_name:str, volume_name:str="") -> str:
  """
    List existing volumes on a given Everpure FlashArray.

    Args:
      array_name: The IP address or FQDN of the management port of the specific Everpure FlashArray. REQUIRED.
      volume_name: The name or partial name of the volumes to be list. Default value is "" means list all volumes on the FlashArray. 
    
    Returns:
      List of names and creation time of the volumes(Latest first). 
  """
  current_array = Get_Array_Info(array_name)
  
  if current_array["array_name"] == "":
    return "ERROR: Array not found in config file. Please add it first!"

  current_client = fatools.Create_FA_Client(current_array)
  results = fatools.Create_One_Volume(current_client,volume_name)
  
  return results


#tool for creating a volume
@mcp.tool()
def Create_One_Volume(array_name:str, volume_name:str, volume_size:int) -> str:
  """
    Create a storage volume on a specific Everpure FlashArray.

    Args:
      array_name: The IP address or FQDN of the management port of the specific Everpure FlashArray. REQUIRED.
      volume_name: The name of the volume. REQUIRED.
      volume_size: The size of the volume. The unit is GB. REQUIRED.

    Returns:
      Results of the job. 
  """
  current_array = Get_Array_Info(array_name)
  
  if current_array["array_name"] == "":
    return "ERROR: Array not found in config file. Please add it first!"

  current_client = fatools.Create_FA_Client(current_array)
  results = fatools.Create_One_Volume(current_client,volume_name, volume_size)
  
  return results

# tools for creating a host
@mcp.tool()
def Create_One_Host(array_name:str, host_name:str, protocol_type:str, endpoint_ids:list[str], personality:str = "") -> str:
  """
    Create a host on a given Everpure FlashArray

    Args:
      array_name: The IP address or FQDN of the management port of the specific Everpure FlashArray. REQUIRED.
      host_name: The name of the host to be created on the array. REQUIRED.
      protocol_type: The protocol to be used to connect host and the array. Should be one of fc/iscsi/nvme. REQUIRED.
      endpoint_ids: The protocol related IDs. WWN for fc, IQN for iscsi, NQN for nvme. REQUIRED.
      personality: Determines how the system tunes the array to ensure that it works optimally with the host. Set personality to the name of the host operating system or virtual memory system. Valid values are aix, esxi, hitachi-vsp, hpux, oracle-vm-server, solaris, vms, nutanix-mgmt and nutanix-cluster. If your system is not listed as one of the valid host personalities, do not set the option. By default, the personality is not set.

    Returns:
      Results of the job.
  """

  # Check if the given array name is in the configuration file
  current_array = Get_Array_Info(array_name)
  if current_array["array_name"] == "":
    return "ERROR: Array not found in config file. Please add it first!"

  current_client = fatools.Create_FA_Client(current_array)
  results = fatools.Create_One_Host(current_client,host_name,protocol_type,endpoint_ids,personality)
  
  return results

# tool for creating a host group
@mcp.tool()
def Create_Host_Group(array_name:str, host_group_name:str) -> str:
  """
    Create a host group on a given Everpure FlashArray

    Args:
      array_name: The IP address or FQDN of the management port of the specific Everpure FlashArray. REQUIRED.
      host_group_name: The name of the host group to be created on the array. REQUIRED.

    Returns:
      Results of the job.
  """

  # Check if the given array name is in the configuration file
  current_array = Get_Array_Info(array_name)
  if current_array["array_name"] == "":
    return "ERROR: Array not found in config file. Please add it first!"

  current_client = fatools.Create_FA_Client(current_array)
  results = fatools.Create_Host_Group(current_client,host_group_name)
  
  return results

# tool for connecting a volume to a host
@mcp.tool()
def Connect_Volume_To_Host(array_name:str,host_name:str, volume_name:str) -> str:
  """
    Connect a pre-created volume to a pre-created host on a specific Everpure FlashArray.

    Args:
      array_name: The IP address or FQDN of the management port of the specific Everpure FlashArray. REQUIRED.
      host_name: The name of the host which was defined on the given Everpure FlashArray and will connect to the given volume. REQUIRED.
      volume_name: The name of the volume which was created before and will be connected to the given host or host group. REQUIRED.

    Returns:
      Results of the job.
  """
  # Check if the given array name is in the configuration file
  current_array = Get_Array_Info(array_name)
  if current_array["array_name"] == "":
    return "ERROR: Array not found in config file. Please add it first!"

  current_client = fatools.Create_FA_Client(current_array)
  results = fatools.Connect_Volume_To_Host(current_client,host_name,volume_name)

  return results

# tool for creating a snapshot from a volume
@mcp.tool()
def Create_Volume_Snapshot(array_name:str, volume_name:str="", snapshot_name:str="") -> str:
  """
    Create a snapshot from a given volume on given Everpure FlashArray.

    Args:
      array name: The IP address or FQDN of the management port of the specific Everpure FlashArray.
      volume name: The name of the volume which snapshot will be created from.
      snapshot name: The name of the snapshot.

    Returns:
      The results of the job.
  """
  current_array = Get_Array_Info(array_name)
  if current_array["array_name"] == "":
    return "ERROR: Array not found in config file. Please add it first!"

  current_client = fatools.Create_FA_Client(current_array)
  results = fatools.Create_Volume_Snapshot(current_client,volume_name,snapshot_name)

  return results

if __name__ == "__main__":
  mcp.run(transport="streamable-http", host="0.0.0.0", port=8765)
