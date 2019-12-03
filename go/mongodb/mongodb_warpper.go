package mongodb


// Environment: go get go.mongodb.org/mongo-driver

import(
	"context"
	"fmt"
	"log"
	"os"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
	"time"
)


type Mongodb struct{
	Mongodb_host string                    `json:"mongodb_host"`
	Mongodb_port string                    `json:"mongodb_port"`
	Mongodb_user string                    `json:"mongodb_user"`
	Mongodb_pwd string                     `json:"mongodb_pwd"`
	Mongodb_name string                    `json:"mongodb_name"`
	MongodbClient *mongo.Client            
	MongodbCollection *mongo.Collection    
	MongodbObj *mongo.Database             
}


const (
	None = ""
)

type MongodbWrapper interface{
	Connectdb() bool
	Close() bool
	InsertOne(collection string,data interface{}) bool 
	InsertMany(collection string,dataList []interface{}) (interface{},error)
	SelectOne(collection string,filter bson.D)(*map[string]interface{},error)
	SelectMany(collection string,filter bson.D,LimitFind int64)(*[]interface{},error)
	UpdateOne(collection string,filter bson.D,update bson.D)(bool,error)
	UpdateMany(collection string,filter bson.D,update bson.D)(bool,error)
	DeleteMany(collection string,filter bson.D)(bool,error)
	FindCount(collection string,filter bson.D)(int64,error)
}

func Init() {}

func(self *Mongodb)InitEnv(){
	self.Mongodb_host =  os.Getenv("MONGODB_HOST")
	self.Mongodb_port = os.Getenv("MONGODB_PORT")
	self.Mongodb_user = os.Getenv("MONGODB_USER")
	self.Mongodb_pwd = os.Getenv("MONGODB_PWD")
	self.Mongodb_name = os.Getenv("MONGODB_NAME")
}

func(self *Mongodb)Connectdb() bool{
// connect to mongo database 
	var mongodb_host string
	// if user authority is not necessary
	if self.Mongodb_user == None && self.Mongodb_pwd == None{
		mongodb_host = fmt.Sprintf("mongodb://%s:%s",self.Mongodb_host,self.Mongodb_port)
	}else{
		// user authority is needed
		mongodb_host = fmt.Sprintf("mongodb://%s:%s@%s:%s/%s",self.Mongodb_user,
															self.Mongodb_pwd,
															self.Mongodb_host,
															self.Mongodb_port,
															self.Mongodb_name)
	}
	ctx , cancel :=context.WithTimeout(context.Background(),10*time.Second)
    defer cancel() 
	clientOptions := options.Client().ApplyURI(mongodb_host)
    client, err := mongo.Connect(ctx, clientOptions)
    if err != nil {
		log.Println(err)
		return false
    }
    err = client.Ping(context.TODO(), nil)
    if err != nil {
		log.Println(err)
		return false
	}
	log.Println("Connected to MongoDB!")
	self.MongodbObj = client.Database(self.Mongodb_name)
	self.MongodbClient = client
	return true
}

func(self *Mongodb)Close() bool{
// close the connection mongo database instance

	if self.MongodbClient == nil{
		return false
	}

	err := self.MongodbClient.Disconnect(context.TODO())
  
	if err != nil {
		log.Println(err)
		return false
	} else {
		log.Println("Connection to MongoDB closed!")
		return true
	}
}

func(self *Mongodb)InsertOne(collection string,data interface{}) bool {
	// how to use it ?
	/*
	type Person struct{
	Name string
	Age int
	}
	one := Person{"xiaoming",16}
	MongodbObj.InsertOne("person",one)
	*/

// you can only insert one data every times
	self.MongodbCollection = self.MongodbObj.Collection(collection)
	_, err := self.MongodbCollection.InsertOne(context.TODO(), data)
	if err != nil{
		log.Println(err)
		return false
	}
	log.Println("Successfully Insert data")
	return true
}

func(self *Mongodb)InsertMany(collection string,dataList []interface{}) (interface{},error){
	// how to use it ?
	/*
	type Person struct{
	Name string
	Age int
	}
	one := Person{"xiaoming",16}
	two := Person{"lilei",18}
	three := Person{"zhangsan",17}
	// MongodbObj.InsertOne("person",one)
	list := []interface{}{one,two,three}
	MongodbObj.InsertMany("person",list) 
	*/

// you can only insert many data every times
	self.MongodbCollection = self.MongodbObj.Collection(collection)
	_, err := self.MongodbCollection.InsertMany(context.TODO(), dataList)
    if err != nil {
	  log.Println(err)
	  return false,err
	  }
	log.Println("Successfully Insert many data")
  	return true,nil
}

func(self *Mongodb)SelectOne(collection string,filter bson.D)(*map[string]interface{},error){
	// how to use this interface? the example as blewo
	/*
	filter := bson.D{{"name", "xiaoming"}}
	result,_ := MongodbObj.SelectOne("person",filter)
	log.Println(*result)
	//how to get the result value according key:
	// data:=*(result.(*map[string]interface{}))
	// data["key"].(interface{})
	*/

// create a value into which the result can be decoded
	self.MongodbCollection = self.MongodbObj.Collection(collection)
	result :=  new(map[string]interface{})

	err := self.MongodbCollection.FindOne(context.TODO(), filter).Decode(result)
	if err != nil {
		log.Println(err)
		return nil,err
	}

	log.Printf("Found a single document: %+v\n", result)
	return result,nil
}

func(self *Mongodb)SelectMany(collection string,filter bson.D,LimitFind int64)(*[]interface{},error){

	//how to use this interface? the example as blewo
	/*
	filter := bson.D{{"name", "xiaoming"}}
	result,_ := MongodbObj.SelectMany("person",filter,0) //0 is mean not limit find
	for _,res:= range *result{
	log.Println((*res.(*map[string]interface{})))
	//how to get the res value according key:
	// data:=*(res.(*map[string]interface{}))
	// data["key"].(interface{})
	}*/


	// Pass these options to the Find method
	findOptions := options.Find()
	findOptions.SetLimit(LimitFind)

	// Here's an array in which you can store the decoded documents
	results := new([]interface{})

	self.MongodbCollection = self.MongodbObj.Collection(collection)

	// Passing bson.D{{}} as the filter matches all documents in the collection
	cur, err := self.MongodbCollection.Find(context.TODO(), filter, findOptions)
	if err != nil {
		log.Println(err)
		return nil,err
	}

	// Finding multiple documents returns a cursor
	// Iterating through the cursor allows us to decode documents one at a time
	for cur.Next(context.TODO()) {
		
		// create a value into which the single document can be decoded
		elem := new(map[string]interface{})
		err := cur.Decode(elem)
		if err != nil {
			log.Println(err)
		}

		*results = append(*results, elem)
	}

	if err := cur.Err(); err != nil {
		log.Println(err)
		return nil,err
	}

	// Close the cursor once finished
	cur.Close(context.TODO())

	log.Printf("Found multiple documents (array of pointers): %+v\n", *results)
	return results,nil
}


func(self *Mongodb)UpdateOne(collection string,filter bson.D,update bson.D)(bool,error){
	// example: update collection set age=1 where name="Ash"
	// filter := bson.D{{"name", "Ash"}}
	// update := bson.D{
	// 	{"$set", bson.D{
	// 		{"age", 1},
	// 	}},
	// }

	self.MongodbCollection = self.MongodbObj.Collection(collection)
	updateResult, err := self.MongodbCollection.UpdateOne(context.TODO(), filter, update)
	if err != nil {
		log.Println(err)
		return false, err
	}
	log.Printf("Matched %v documents and updated %v documents.\n", updateResult.MatchedCount, updateResult.ModifiedCount)
	return true, nil
}

func(self *Mongodb)UpdateMany(collection string,filter bson.D,update bson.D)(bool,error){
	// example: update collection set age=1 where name="Ash"
	// filter := bson.D{{"name", "Ash"}}
	// update := bson.D{
	// 	{"$set", bson.D{
	// 		{"age", 1},
	// 	}},
	// }

	self.MongodbCollection = self.MongodbObj.Collection(collection)
	updateResult, err := self.MongodbCollection.UpdateMany(context.TODO(), filter, update)
	if err != nil {
		log.Println(err)
		return false, err
	}
	log.Printf("Matched %v documents and updated %v documents.\n", updateResult.MatchedCount, updateResult.ModifiedCount)
	return true, nil
}

func(self *Mongodb)DeleteMany(collection string,filter bson.D)(bool,error){

	self.MongodbCollection = self.MongodbObj.Collection(collection)
	deleteResult, err := self.MongodbCollection.DeleteMany(context.TODO(), filter)
	if err != nil {
		log.Println(err)
		return false,err
	}
	log.Printf("Deleted %v documents in the trainers collection\n", deleteResult.DeletedCount)
	return true, nil
}

func(self *Mongodb)FindCount(collection string,filter bson.D)(int64,error){
	
	self.MongodbCollection = self.MongodbObj.Collection(collection)
    count, err := self.MongodbCollection.CountDocuments(context.TODO(),filter)
	if err != nil {
		log.Println(err)
		return -1,err
	}
	log.Printf("Count find:%d numbers\n", count)
	return count,nil
}