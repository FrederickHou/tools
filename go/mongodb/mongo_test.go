package mongodb

import(
	"fmt"
	"mongodb"
	"go.mongodb.org/mongo-driver/bson"
)

func main() {

	var MongodbObj mongodb.Mongodb
	MongodbObj.Mongodb_host="127.0.0.1"
	MongodbObj.Mongodb_port="27017"
	MongodbObj.Mongodb_user="test"
	MongodbObj.Mongodb_pwd="test"
	MongodbObj.Mongodb_name="test"
	MongodbObj.Connectdb()
	defer MongodbObj.Close()
	type Person struct{
		Name string
		Age int
	}
	one := Person{}
	two := Person{"lilei",18}
	three := Person{"zhangsan",17}

	MongodbObj.InsertOne("person",one)

	list := []interface{}{one,two,three}
	MongodbObj.InsertMany("person",list) 

	filter := bson.D{{"name", "xiaoming"}}
	MongodbObj.FindCount("person",filter)

	result,_ := MongodbObj.SelectOne("person",filter)
	fmt.Println(json.Get(result,"key"))

	result,_ := MongodbObj.SelectMany("person",filter,0)
	for _,res:= range *result{
		fmt.Println(res)
	}

}