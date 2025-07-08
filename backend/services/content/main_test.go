package main

import "testing"

func TestGenIDUnique(t *testing.T) {
    id1 := genID()
    id2 := genID()
    if id1 == id2 {
        t.Fatalf("expected unique ids")
    }
}
