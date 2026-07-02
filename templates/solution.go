// <Problem Title>
// <url>
//
// <problem statement — paste here>
package main

import (
	"fmt"
	"os"
	"reflect"
)

// --- tiny inline test helper (Go's tooling makes a shared cross-dir one awkward) ---
var failed int

func check(name string, got, want interface{}) {
	if reflect.DeepEqual(got, want) {
		fmt.Printf("✅ %s passed\n", name)
	} else {
		failed++
		fmt.Printf("❌ %s failed\n   Expected: %v\n   Got:      %v\n", name, want, got)
	}
}

func solve( /* args */ ) interface{} {
	// Explain the approach. Time O(?), Space O(?).
	return nil
}

func main() {
	// check("Example 1", solve(/* args */), want)

	if failed > 0 {
		os.Exit(1)
	}
	fmt.Println("All tests passed! 🎉")
}
