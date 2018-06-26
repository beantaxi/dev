package main
// Create a new go file
// Read the just like in the other thing
// Use decoder, see what happens
// - It should output objects
// Try and read specific objects

import (
	"encoding/json"
	"fmt"
	//"io/ioutil"
	"os"
	"strings"
	"time"
)

type Thing struct {
	Id, Name string
}
const format = "2006-01-02T15:04:05.000"

type CustomTime struct {
    time.Time
}

func (ct *CustomTime) UnmarshalJSON(b []byte) (err error) {
    s := strings.Trim(string(b), "\"")
    if s == "null" {
       ct.Time = time.Time{}
       return
	}
	if iLast := strings.LastIndex(s, "."); iLast == -1 {
		s = s + ".000"
	} else {
		nZeroes := len(s) - (iLast+1)
		fmt.Printf("s=%s nZeroes=%d\n", s, nZeroes)
		for i:=nZeroes; i<3; i++ {
			s += "0"
		}
	}
    ct.Time, err = time.Parse(format, s)
    return
}

func (ct *CustomTime) MarshalJSON() ([]byte, error) {
  if ct.Time.UnixNano() == nilTime {
    return []byte("null"), nil
  }
  return []byte(fmt.Sprintf("\"%s\"", ct.Time.Format(format))), nil
}

var nilTime = (time.Time{}).UnixNano()

type Organization struct {
	Id	string
	Name string
	Slug string
	InProduction bool
	InsertedAt time.Time
	InsertedBy string
	UpdatedAt time.Time
	UpdatedBy string
}

type User struct {
	Id string
	OrganizationId string
	PasswordHash string
	Email string
	FirstName string
	LastName string
	Position string
	Biography string
	Picture string
	IsVerified bool
	IsDeleted bool
	InsertedAt string
	InsertedBy string
	UpdatedAt string
	UpdatedBy string
}

type Employee struct {
	Id string
	OrgName string
	UserEmail string
}


func openDecoder (path string) *json.Decoder {
	f, _ := os.Open(path)
	var decoder *json.Decoder = json.NewDecoder(f)
	return decoder 
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
		fmt.Printf("%T %s\n", o, o.Id)
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
		fmt.Printf("%T %s\n", o, o.Id)
	}
}

func testDateFormat () {

}


func main () {
	doOrganizations()
	doUsers()
//	testDateFormat()
}