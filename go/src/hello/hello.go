package main

import (
	"fmt"
	"io/ioutil"
//	"net/http"
//	"strconv"
	"github.com/valyala/fastjson"
	"github.com/go-resty/resty"
)

func sliceThings () {
	fmt.Println("Hello World!")
	homeSlice := []int{1, 2, 3, 4, 5}
	fmt.Println(len(homeSlice))
	slice := homeSlice[:len(homeSlice)]
	fmt.Println(slice)

	secondSlice := make([]int, 5, 10)
	fmt.Println(secondSlice)
	fmt.Printf("len=%d cap=%d\n", len(secondSlice), cap(secondSlice))
	thirdSlice := secondSlice[len(secondSlice): cap(secondSlice)]
	thirdSlice[2] = 13
	fmt.Println(thirdSlice)
	fmt.Printf("len=%d cap=%d\n", len(thirdSlice), cap(thirdSlice))
	secondSlice = secondSlice[:cap(secondSlice)] 
	secondSlice[7] = 169
	fmt.Println(secondSlice)
	fmt.Printf("len=%d cap=%d\n", len(secondSlice), cap(secondSlice))
	lastSlice := make([]int, len(secondSlice))
	copy(lastSlice, secondSlice)
	secondSlice[len(secondSlice)-1] = 1881
	fmt.Println(secondSlice)
	fmt.Printf("len=%d cap=%d\n", len(secondSlice), cap(secondSlice))
	fmt.Println(lastSlice)
	fmt.Printf("len=%d cap=%d\n", len(lastSlice), cap(secondSlice))
}

func mapThings () {
	d := make(map [string] int)
	d["luckyNumber"] = 13
	fmt.Println(d)
	fmt.Println(len(d))
	delete(d, "Lucky Number")
	fmt.Println(d)
	fmt.Println(len(d))
}



func fileThings () {
	data, err := ioutil.ReadFile("/tmp/orgs.json")
	if err != nil {
		panic(err)
	}

	var parser  fastjson.Parser
	v, err := parser.Parse(string(data[:]))
	if err != nil {
		panic(err)
	}

	a, err := v.Array()
	if err != nil {
		panic(err)		
	}

	fmt.Println(len(a))
	for _, o := range a {
		fmt.Printf("o's type=%T\n", o)
		obj := o.GetObject()
		fmt.Printf("len=%d\n", obj.Len())
		fmt.Printf("len=%s type=%T\n", obj.Get("Id"), obj.Get("Id"))
		org := Organization {
		Id : string(o.Get("Id").GetStringBytes()[:]),
		Name : string(o.Get("Name").GetStringBytes()[:]),
		Slug : string(o.Get("Slug").GetStringBytes()[:]),
		InProduction : o.GetBool("InProduction"),
		}
		fmt.Println(org)
//		user := User{Username: "testuser", Password: "testpass"}
		PostOrg(org)
//		PostOrg(user)
	}
}

type AuthSuccess struct {
	ID, Message string
}
type Organization struct {
	Id           string `json:"id"`
	Name         string `json:"name"`
	Slug         string `json:slug`
	InProduction bool   `json:inProduction`
}

type User struct {
	Id, Name, Slug string
}

func PostOrg (org Organization) {
//func PostOrg (user User) {
//	fmt.Printf("%s %s (%s) %t\n", org.id, org.name, org.slug, org.inProduction)
//	body := make(map [string] string)
//	body["id"] = org.id
//	body["name"] = org.name
//	body["slug"] = org.slug
//	body["inProduction"] = strconv.FormatBool(org.inProduction)
	var resp *resty.Response
//	fmt.Println(org)
//	user := User{Id: "test", Name: "test", Slug: "test"}
	resp, err := resty.R().
				 SetHeader("Content-Type", "application/json").
				 SetBody(org).
//				 SetBody(user).
//				 SetBody(body).
				 SetResult(&AuthSuccess{}).
				 Post("http://localhost:5000/organizations")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Printf("%3d %s\n", resp.StatusCode(), resp.Status())
//	fmt.Println(string(resp.Body()[:]))
//	var header http.Header = resp.Header()
//	for k, v := range header {
//		fmt.Printf("%-32s %-32s\n", k, v)
//	}
}

func objThings () {
	org := Organization {
		Id : "id",
		Name : "name",
		Slug : "slug",
		InProduction : false,
	}
	printOrg(&org)
}

func printOrg (org* Organization) {
	fmt.Println(*org)
}

func main () {
	fileThings()
//	objThings()
}