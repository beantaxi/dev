package main

import (
	"fmt"
	"io/ioutil"
//	"net/http"
	"strconv"
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
	for _, org := range a {
		id := org.GetStringBytes("Id")
		name := org.GetStringBytes("Name")
		slug := org.GetStringBytes("Slug")
		inProduction := org.GetBool("InProduction")
		PostOrg(id, name, slug, inProduction)
	}
}


func PostOrg (id []byte, name []byte, slug []byte, inProduction bool) {
	fmt.Printf("%s %s (%s) %t\n", id, name, slug, inProduction)
	body := make(map [string] string)
	body["id"] = string(id[:])
	body["name"] = string(name[:])
	body["slug"] = string(name[:])
	body["inProduction"] = strconv.FormatBool(inProduction)
	var resp *resty.Response
	resp, err := resty.R().
				 SetHeader("Content-Type", "application/json").
				 SetBody(body).
				 SetResult("Ok!").
				 Post("http://localhost:5000/organizations")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Printf("%3d %s\n", resp.StatusCode(), resp.Status())
	fmt.Println(string(resp.Body()[:]))
//	var header http.Header = resp.Header()
//	for k, v := range header {
//		fmt.Printf("%-32s %-32s\n", k, v)
//	}
}

func main () {
	fileThings()
}