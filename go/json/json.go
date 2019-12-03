package json

import (
    "encoding/json"
    "log"
    "io/ioutil"
    "os"
)

func init(){}

func Loadjson(filename string,obj interface{})error{

	// Open our jsonFile
	jsonFile, err := os.Open(filename)
	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()
	// if we os.Open returns an error then handle it
	if err != nil {
		log.Println(err)
		return err
	}
	// read our opened jsonFile as a byte array.
	byteValue, _ := ioutil.ReadAll(jsonFile)
	// we unmarshal our byteValue to json format
	json.Unmarshal(byteValue,&obj)
	return nil
}

func Loadjson_s(filename string)(*map[string]interface{},error){
	// the *map[string]interface{} should use this example to get value
	// jsonObjPoint,_ := json.Loadjson_s(ConfigPath)
	// (*jsonObjPoint)["mongodb_port"].(interface{})

	jsonObjPoint := new(map[string]interface{})
	// Open our jsonFile
	jsonFile, err := os.Open(filename)
	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()
	// if we os.Open returns an error then handle it
	if err != nil {
		log.Println(err)
		return nil,err
	}
	// read our opened jsonFile as a byte array.
	byteValue, _ := ioutil.ReadAll(jsonFile)
	// we unmarshal our byteValue to json format
	json.Unmarshal(byteValue,jsonObjPoint)
	return jsonObjPoint,nil
}

func LoadjsonByteArray(data []byte)(*map[string]interface{}){
	jsonObjPoint :=new(map[string]interface{})
	json.Unmarshal(data,jsonObjPoint)
	return jsonObjPoint
}


func Get(jsondata interface{},key string,defaultValue interface{})(interface{}){
	// assert jsondata type to *map[string]interface{}
	mapdata:=*(jsondata.(*map[string]interface{}))
	if _, ok := mapdata[key]; ok {
		value := mapdata[key].(interface{})
		return value
	}else{
		return defaultValue
	}
}

func Dumpjson(data interface{})(string,error){
	
	jsondata,err := json.Marshal(data)
	if err != nil{
		return "",err
	}
	return string(jsondata),nil
}
