package main

import (
	"encoding/json"
	"fmt"
	"os"
//	"io/ioutil"
//	"net/http"
//	"strconv"
//	"time"
//	"github.com/valyala/fastjson"
	"github.com/go-resty/resty"
)

// func sliceThings () {
// 	fmt.Println("Hello World!")
// 	homeSlice := []int{1, 2, 3, 4, 5}
// 	fmt.Println(len(homeSlice))
// 	slice := homeSlice[:len(homeSlice)]
// 	fmt.Println(slice)
// 
// 	secondSlice := make([]int, 5, 10)
// 	fmt.Println(secondSlice)
// 	fmt.Printf("len=%d cap=%d\n", len(secondSlice), cap(secondSlice))
// 	thirdSlice := secondSlice[len(secondSlice): cap(secondSlice)]
// 	thirdSlice[2] = 13
// 	fmt.Println(thirdSlice)
// 	fmt.Printf("len=%d cap=%d\n", len(thirdSlice), cap(thirdSlice))
// 	secondSlice = secondSlice[:cap(secondSlice)] 
// 	secondSlice[7] = 169
// 	fmt.Println(secondSlice)
// 	fmt.Printf("len=%d cap=%d\n", len(secondSlice), cap(secondSlice))
// 	lastSlice := make([]int, len(secondSlice))
// 	copy(lastSlice, secondSlice)
// 	secondSlice[len(secondSlice)-1] = 1881
// 	fmt.Println(secondSlice)
// 	fmt.Printf("len=%d cap=%d\n", len(secondSlice), cap(secondSlice))
// 	fmt.Println(lastSlice)
// 	fmt.Printf("len=%d cap=%d\n", len(lastSlice), cap(secondSlice))
// }
// 
// func mapThings () {
// 	d := make(map [string] int)
// 	d["luckyNumber"] = 13
// 	fmt.Println(d)
// 	fmt.Println(len(d))
// 	delete(d, "Lucky Number")
// 	fmt.Println(d)
// 	fmt.Println(len(d))
// }
// 


// func fileThings () {
// 	data, err := ioutil.ReadFile("/tmp/orgs.json")
// 	if err != nil {
// 		panic(err)
// 	}
// 
// 	var parser  fastjson.Parser
// 	v, err := parser.Parse(string(data[:]))
// 	if err != nil {
// 		panic(err)
// 	}
// 
// 	a, err := v.Array()
// 	if err != nil {
// 		panic(err)		
// 	}
// 
// 	fmt.Println(len(a))
// 	for _, o := range a {
// 		fmt.Printf("o's type=%T\n", o)
// 		obj := o.GetObject()
// 		fmt.Printf("len=%d\n", obj.Len())
// 		fmt.Printf("len=%s type=%T\n", obj.Get("Id"), obj.Get("Id"))
// //		org := Organization {
// //		Id : string(o.Get("Id").GetStringBytes()[:]),
// //		Name : string(o.Get("Name").GetStringBytes()[:]),
// //		Slug : string(o.Get("Slug").GetStringBytes()[:]),
// //		InProduction : o.GetBool("InProduction"),
// 		}
// 		fmt.Println(org)
// //		user := User{Username: "testuser", Password: "testpass"}
// 		PostOrg(org)
// //		PostOrg(user)
// 	}
// }

type AuthSuccess struct {
	ID, Message string
}

// type Employee struct {
// 	Id           string    `json:"id"`
// 	InsertedBy   string    `json:"insertedBy"`
// 	UpdatedBy    string    `json:"updatedBy"`
// }
// 
// type Organization struct {
// 	Id           string    `json:"id"`
// 	Name         string    `json:"name"`
// 	Slug         string    `json:"slug"`
// 	InProduction bool      `json:"inProduction"`
// 	InsertedBy   string    `json:"insertedBy"`
// 	UpdatedBy    string    `json:"updatedBy"`
// }
// 
// type User struct {
// 	Id             string    `json:"id"`
// 	OrganizationId string    `json:"organizationId"`
// 	PasswordHash   string    `json:"passwordHash"`
// 	Email          string    `json:"email"`
// 	FirstName      string    `json:"firstName"`
// 	LastName       string    `json:"lastName"`
// 	Position       string    `json:"position"`
// 	Biography      string    `json:"biography"`
// 	Picture        string    `json:"picture"`
// 	IsVerified     bool      `json:"isVerified"`
// 	InsertedBy     string    `json:"insertedBy"`
// 	UpdatedBy      string    `json:"updatedBy"`
// }

type Organization struct {
	Id              string    `json:"Id"`
	Name            string    `json:"Name"`
	Slug            string    `json:"Slug"`
	InProduction    bool      `json:"InProduction"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type User struct {
	Id              string    `json:"Id"`
	OrganizationId  string    `json:"OrganizationId"`
	PasswordHash    string    `json:"PasswordHash"`
	Email           string    `json:"Email"`
	FirstName       string    `json:"FirstName"`
	LastName        string    `json:"LastName"`
	Position        string    `json:"Position"`
	Biography       string    `json:"Biography"`
	Picture         string    `json:"Picture"`
	IsVerified      bool      `json:"IsVerified"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
	UserMetadata    string    `json:"UserMetadata"`
	AppMetadata     string    `json:"AppMetadata"`
}

type Employee struct {
	Id              string    `json:"id"`
	OrgName         string    `json:"orgName"`
	UserEmail       string    `json:"userEmail"`
}

type Role struct {
	Id              string    `json:"Id"`
	OrganizationId  string    `json:"OrganizationId"`
	IsAdministrator bool      `json:"IsAdministrator"`
	Name            string    `json:"Name"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type EmployeeRole struct {
	EmployeeId      string    `json:"EmployeeId"`
	RoleId          string    `json:"RoleId"`
}

type Permission struct {
	Id              string    `json:"Id"`
	Name            string    `json:"Name"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type Resource struct {
	Id              string    `json:"Id"`
	Url             string    `json:"Url"`
	UrlRegex        string    `json:"UrlRegex"`
	Method          string    `json:"Method"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type Agent struct {
	Id              string    `json:"Id"`
	OrganizationId  string    `json:"OrganizationId"`
	Name            string    `json:"Name"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type PermissionResource struct {
	PermissionId    string    `json:"PermissionId"`
	ResourceId      string    `json:"ResourceId"`
}

type RolePermission struct {
    RoleId          string    `json:"RoleId"`
	PermissionId    string    `json:"PermissionId"`
}

type Asset struct {
	Id              string    `json:"Id"`
	ParentId        string    `json:"ParentId"`
	OrganizationId  string    `json:"OrganizationId"`
	Name            string    `json:"Name"`
	Description     string    `json:"Description"`
	Metadata        string    `json:"Metadata"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type Tag struct {
	Id              string    `json:"Id"`
	AgentId         string    `json:"AgentId"`
	AssetId         string    `json:"AssetId"`
	OrganizationId  string    `json:"OrganizationId"`
	TagId           string    `json:"TagId"`
	DefaultValue    string    `json:"DefaultValue"`
	Description     string    `json:"Description"`
	Type            string    `json:"Type"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type ModelAction struct {
	Id              string    `json:"Id"`
	ModelId         string    `json:"ModelId"`
	OrganizationId  string    `json:"OrganizationId"`
	Body            string    `json:"Body"`
	ContentType     string    `json:"ContentType"`
	Method          string    `json:"Method"`
	Scope           string    `json:"Scope"`
	ScopeList       string    `json:"ScopeList"`
	Name            string    `json:"Name"`
	Queue           string    `json:"Queue"`
	Type            string    `json:"Type"`
	Url             string    `json:"Url"`
	Version         string    `json:"Version"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type Pipeline struct {
	Id              string    `json:"Id"`
	OrganizationId  string    `json:"OrganizationId"`
	OwnerId         string    `json:"OwnerId"`
	Version         string    `json:"Version"`
 	IsActive        bool      `json:"IsActive"`
  	Name            string    `json:"Name"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type Parameter struct {
	Id              string    `json:"Id"`
	ModelActionId   string    `json:"ModelActionId"`
	OrganizationId  string    `json:"OrganizationId"`
	OwnerId         string    `json:"OwnerId"`
	ParentId        string    `json:"ParentId"`
	PipelineId      string    `json:"PipelineId"`
	Version         string    `json:"Version"`
	InsertedBy      string    `json:"InsertedBy"`
	UpdatedBy       string    `json:"UpdatedBy"`
}

type Input struct {
   Id              string    `json:"Id"`
   ModelActionId   string    `json:"ModelActionId"`
   OrganizationId  string    `json:"OrganizationId"`
   Name            string    `json:"Name"`
   Type            string    `json:"Type"`
   InsertedBy      string    `json:"InsertedBy"`
   UpdatedBy       string    `json:"UpdatedBy"`
}

type Output struct {
   Id              string    `json:"Id"`
   ModelActionId   string    `json:"ModelActionId"`
   OrganizationId  string    `json:"OrganizationId"`
   Name            string    `json:"Name"`
   Type            string    `json:"Type"`
   InsertedBy      string    `json:"InsertedBy"`
   UpdatedBy       string    `json:"UpdatedBy"`
}

type InputConnection struct {
   Id              string    `json:"Id"`
   InputId         string    `json:"InputId"`
   OrganizationId  string    `json:"OrganizationId"`
   ParameterId     string    `json:"ParameterId"`
   TagId           string    `json:"TagId"`
   InsertedBy      string    `json:"InsertedBy"`
   UpdatedBy       string    `json:"UpdatedBy"`
}

type OutputConnection struct { 
   Id              string    `json:"Id"`
   OrganizationId  string    `json:"OrganizationId"`
   OutputId        string    `json:"OutputId"`
   ParameterId     string    `json:"ParameterId"`
   TagId           string    `json:"TagId"`
   InsertedBy      string    `json:"InsertedBy"`
   UpdatedBy       string    `json:"UpdatedBy"`
}

type ModelStatus struct {
	Id              string    `json:"Id"`
	Name            string    `json:"Name"`
}


func openDecoder (path string) *json.Decoder {
	f, _ := os.Open(path)
	var decoder *json.Decoder = json.NewDecoder(f)
	return decoder 
}


func doEmployees () {
	decoder := openDecoder("/tmp/employees.json")
	var data []Employee
	err := decoder.Decode(&data)
	if err != nil {
		panic(err)
	}
	fmt.Printf("type=%T\n", data)
	for _, o := range(data) {
		fmt.Println(o)
		Post("http://localhost:5000/employees", o)
	}
}

func doUsers () {
	decoder := openDecoder("/tmp/users.json")
	var data []User
	err := decoder.Decode(&data)
	if err != nil {
		panic(err)
	}
	fmt.Printf("type=%T\n", data)
	for _, o := range(data) {
		Post("http://localhost:5000/users", o)
	}
}


func doOrganizations () {
	decoder := openDecoder("/tmp/orgs.json")
	var data []Organization
	err := decoder.Decode(&data)
	if err != nil {
		panic(err)
	}
	fmt.Printf("type=%T\n", data)
	for _, o := range(data) {
		Post("http://localhost:5000/organizations", o)
	}
}


func Post (url string, o interface{}) {
	resp, err := resty.R().
				 SetHeader("Content-Type", "application/json").
				 SetBody(o).
				 SetResult(&AuthSuccess{}).
				 Post(url)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Printf("%3d %s\n", resp.StatusCode(), resp.Status())
}

// func PostUser (o User) {
// 	resp, err := resty.R().
// 				 SetHeader("Content-Type", "application/json").
// 				 SetBody(user).
// 				 SetResult(&AuthSuccess{}).
// 				 Post("http://localhost:5000/users")
// 	if err != nil {
// 		fmt.Println(err)
// 	}
// 	fmt.Printf("%3d %s\n", resp.StatusCode(), resp.Status())
// }

// func objThings () {
// 	org := Organization {
// 		Id : "id",
// 		Name : "name",
// 		Slug : "slug",
// 		InProduction : false,
// 	}
// 	printOrg(&org)
// }

func printOrg (org* Organization) {
	fmt.Println(*org)
}


func PostThings () {
//	doOrganizations()
//	doUsers()
	doEmployees()
}
func main () {
//	fileThings()
//	objThings()
	PostThings()
}