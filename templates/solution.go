// <Problem Title>
// <url>
//
// <problem statement — paste here>
package main

import (
	"fmt"
	"os"
	"reflect"
	"strings"
)

// --- tiny inline test helper (Go's tooling makes a shared cross-dir one awkward) ---
var failed int

func check(name string, got, want interface{}) {
	if reflect.DeepEqual(got, want) {
		fmt.Printf("✅  %s\n", name)
	} else {
		failed++
		fmt.Printf("❌  %s\n      expected: %v\n      got:      %v\n", name, want, got)
	}
}

func solve( /* args */ ) interface{} {
	// Explain the approach. Time O(?), Space O(?).
	return nil
}

func main() {
	// check("Example 1", solve(/* args */), want)

	fmt.Println("\n" + strings.Repeat("─", 34))
	if failed > 0 {
		fmt.Printf("❌  %d test(s) failed\n", failed)
		os.Exit(1)
	}
	fmt.Println("🎉  all tests passed — all green")
}
