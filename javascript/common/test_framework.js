// Minimal test helper — the JavaScript counterpart of the other common/ helpers.
// Solutions load it via NODE_PATH (set by run.py) as:
//   const { runTests } = require("common/test_framework");
// Prints ✅/❌ per case and exits non-zero if any case fails.
function runTests(cases) {
  let passed = 0;
  const failures = [];
  const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);

  for (const [fn, args, expected, name] of cases) {
    const got = fn(...args);
    if (eq(got, expected)) {
      passed++;
      console.log(`✅ ${name} passed`);
    } else {
      failures.push(name);
      console.log(`❌ ${name} failed`);
      console.log(`   Expected: ${JSON.stringify(expected)}`);
      console.log(`   Got:      ${JSON.stringify(got)}`);
    }
  }

  console.log(`\nTest Results: ${passed}/${cases.length} passed`);
  if (failures.length) {
    console.log(`${failures.length} test(s) failed`);
    process.exit(1);
  }
  console.log("All tests passed! 🎉");
}

module.exports = { runTests };
