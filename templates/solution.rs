// <Problem Title>
// <url>
//
// <problem statement — paste here>

// --- tiny inline test helper (self-contained; compiled with `rustc`) ---
fn check<T: std::fmt::Debug + PartialEq>(name: &str, got: T, want: T, failed: &mut u32) {
    if got == want {
        println!("✅  {}", name);
    } else {
        *failed += 1;
        println!("❌  {}\n      expected: {:?}\n      got:      {:?}", name, want, got);
    }
}

fn solve(/* args */) {
    // Explain the approach. Time O(?), Space O(?).
}

fn main() {
    let mut failed: u32 = 0;
    // check("Example 1", solve(/* args */), want, &mut failed);

    println!("\n{}", "─".repeat(34));
    if failed > 0 {
        println!("❌  {} test(s) failed", failed);
        std::process::exit(1);
    }
    println!("🎉  all tests passed — all green");
}
