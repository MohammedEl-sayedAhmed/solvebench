// <Problem Title>
// <url>
//
// <problem statement — paste here>

// --- tiny inline test helper (self-contained; compiled with `rustc`) ---
fn check<T: std::fmt::Debug + PartialEq>(name: &str, got: T, want: T, failed: &mut u32) {
    if got == want {
        println!("✅ {} passed", name);
    } else {
        *failed += 1;
        println!("❌ {} failed\n   Expected: {:?}\n   Got:      {:?}", name, want, got);
    }
}

fn solve(/* args */) {
    // Explain the approach. Time O(?), Space O(?).
}

fn main() {
    let mut failed: u32 = 0;
    // check("Example 1", solve(/* args */), want, &mut failed);

    if failed > 0 {
        std::process::exit(1);
    }
    println!("All tests passed! 🎉");
}
