package main

import (
	"fmt"
	"time"
)

func main () {
//	const s      = "2018-06-25T03:02:24.923"
	const s      = "2018-06-24T22:59:42.040"
	const format = "2006-01-02T15:04:05.000"
	var t time.Time
	t, err := time.Parse(format, s)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Printf("%T\n", t)
	}
}