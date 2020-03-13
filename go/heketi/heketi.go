package main


import (
	"fmt"
	"errors"
	client"github.com/heketi/heketi/client/api/go-client"
	api"github.com/heketi/heketi/pkg/glusterfs/api"
)

type Heketi struct{
	Url string
	User string
	Key string
	ClientObj *client.Client
}

func(self *Heketi)NewClient(){
    // Create a client object
	clientObj := client.NewClient(self.Url, self.User, self.Key)
	self.ClientObj = clientObj
}

func(self *Heketi)CreateCluster(block bool,file bool)(string,error){
	// create a cluster
	clusterCreateReq := &api.ClusterCreateRequest{}
	clusterCreateReq.ClusterFlags.Block = true
	clusterCreateReq.ClusterFlags.File = true
	clusterInfoRep,err := self.ClientObj.ClusterCreate(clusterCreateReq)
	return clusterInfoRep.Id,err
}

func(self *Heketi)ClusterList()([]string,error){
	// Get  cluster list
	clusterListRes,err := self.ClientObj.ClusterList()
	if err != nil{
		return nil,err
	}
	if len((*clusterListRes).Clusters) == 0{
		fmt.Println("don't have a cluster")
		return []string{},errors.New("don't have a cluster")
	}
	clusterList := (*clusterListRes).Clusters
	return clusterList,nil
}


func(self *Heketi)ClusterInfo(clusterId string)([]string,[]string,[]string,error){
	clusterInfoRes,err := self.ClientObj.ClusterInfo(clusterId)
	return clusterInfoRes.Nodes,clusterInfoRes.Volumes ,clusterInfoRes.BlockVolumes ,err
}

func(self *Heketi)AddNode(clusterId string,zone int,hostnameManage []string,hostnamesStorage []string,Tags map[string]string)(*api.NodeInfoResponse,error){
	// Create node
	nodeReq := &api.NodeAddRequest{}
	nodeReq.ClusterId = clusterId
	nodeReq.Hostnames.Manage = []string{"cent" + fmt.Sprintf("%v", zone)}
	nodeReq.Hostnames.Storage = []string{"storage" + fmt.Sprintf("%v", zone)}
	nodeReq.Zone = zone + 1
	nodeReq.Tags = Tags
	// Add node
	node, err := self.ClientObj.NodeAdd(nodeReq)
	return node ,err
}

func(self *Heketi)AddDevice(nodeId string, deviceName string)(bool,error){
		// add device
		deviceReq := &api.DeviceAddRequest{}
		deviceReq.Name = deviceName
		deviceReq.NodeId = nodeId
		err := self.ClientObj.DeviceAdd(deviceReq)
		if err != nil{
			return false,err
		}
		return true,nil
}

func(self *Heketi)VolumeCreate(size int,name string,replica int,clustersIdList []string,block bool)(string,error){
	volumeCreateReq := &api.VolumeCreateRequest{} 
	volumeCreateReq.Size = size
	volumeCreateReq.Clusters = clustersIdList
	volumeCreateReq.Name = name
	volumeCreateReq.Block  = block
	volumeCreateReq.Durability.Replicate.Replica = replica
	volumeInfoRes := &api.VolumeInfoResponse{}
	volumeInfoRes,err := self.ClientObj.VolumeCreate(volumeCreateReq)
	return volumeInfoRes.VolumeInfo.Id,err
}

func(self *Heketi)VolumeDelete(id string)(error){
	return self.ClientObj.VolumeDelete(id)
}

func(self *Heketi)VolumeInfo(id string){
	info,_ := self.ClientObj.VolumeInfo(id)
	fmt.Println(info)
}


func(self *Heketi)GetClusterInfoDetail(clusterId string)(map[string]interface{}){

	/*
		{
			"ClusterId":"",
			"ClusterInfo":[
				{
					"NodeName":"",
					"NodeId":"",
					"NodeState":"",
					"DevideInfo":[
					{
						"DeviceId":"",
						"DeviceName":"",
						"DeviceState":"",
						"DeviceTotal":0,
						"DeviceUsed":0,
						"DeviceFree":0,
					}
				]
				}
			]
		}
	*/
	clusterInfo,_ := self.ClientObj.ClusterInfo(clusterId)
	clusterInfoDetailMap := map[string]interface{}{}
	var nodeList  []interface{}
	clusterInfoDetailMap["ClusterId"] = clusterId
	//select  cluster's node
	for _,node:= range clusterInfo.Nodes {
		nodeInfoRes ,_:= self.ClientObj.NodeInfo(node) 
		var newdDviceInfoList  []interface{}
		newNodeInfo := map[string]interface{}{}
		newNodeInfo["NodeState"] = (*nodeInfoRes).State
		newNodeInfo["NodeId"] = (*nodeInfoRes).NodeInfo.Id
		newNodeInfo["NodeName"] = (*nodeInfoRes).NodeInfo.NodeAddRequest.Hostnames.Manage
		devicesInfoResList := (*nodeInfoRes).DevicesInfo   
		for _,deviceInfoRes := range devicesInfoResList{
			deviceInfo := map[string]interface{}{}
			deviceInfo["DeviceId"] = deviceInfoRes.DeviceInfo.Id
			deviceInfo["DeviceName"] = deviceInfoRes.DeviceInfo.Device.Name
			deviceInfo["DeviceUsed"] = deviceInfoRes.DeviceInfo.Storage.Used
			deviceInfo["DeviceFree"] = deviceInfoRes.DeviceInfo.Storage.Free
			deviceInfo["DeviceTotal"] = deviceInfoRes.DeviceInfo.Storage.Total 
			deviceInfo["DeviceState"] = deviceInfoRes.State
			newdDviceInfoList = append(newdDviceInfoList,deviceInfo)
	        newNodeInfo["DevideInfo"] = newdDviceInfoList											
		}
		nodeList = append(nodeList,newNodeInfo)
	}
	clusterInfoDetailMap["ClusterInfo"] = nodeList
	return clusterInfoDetailMap
}

