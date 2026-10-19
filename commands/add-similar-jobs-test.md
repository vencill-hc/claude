# add-similar-jobs-test

Add a new test case to the similar jobs evaluation suite from a natural language description

## Arguments
`$ARGUMENTS` - Natural language description of the test case

## Steps I will take:
1. Parse the description provided in $ARGUMENTS to extract:
   - Job titles (source and target)
   - Locations
   - Company details (stage, size)
   - Expected similarity level
   - Special conditions (missing JD, remote/onsite, PE/VC backed, etc.)

2. Interpret similarity expectations:
   - "should match highly" / "high match" → 75-90%
   - "should match moderately" / "medium match" → 60-75%
   - "should have low match" / "low similarity" → 10-30%
   - "should conflict" / "should not match" → 5-20%
   - "similar roles" → 60-75%
   - "different functions" → 10-30%

3. Generate test case structure with:
   - Unique test name based on the description
   - Source job configuration
   - Target job(s) configuration
   - Expected score ranges
   - Expected reasons based on common attributes

4. Append the new test case to `config/similar_jobs_eval.yml`

5. Show the generated test case for confirmation

6. Optionally run the new test immediately to verify it works

## Example usage:
```
/add-similar-jobs-test "software engineer and senior software engineer both missing JD in same location should match highly"

/add-similar-jobs-test "remote DevOps vs onsite SRE should have medium match despite location difference"

/add-similar-jobs-test "PE-backed CFO and VC-backed startup CFO in NYC should have low-medium match"

/add-similar-jobs-test "product manager and engineering manager at same company stage should have low match"

/add-similar-jobs-test "data scientist and machine learning engineer with similar requirements should match well"
```

## Natural language patterns I understand:
- **Roles**: "software engineer", "product manager", "DevOps", "SRE", "CFO", etc.
- **Seniority**: "senior", "junior", "staff", "principal", "manager", "director", "VP"
- **Location**: "in SF", "in same location", "both in NYC", "remote", "onsite"
- **Company**: "similar stage", "Series A", "PE-backed", "VC-backed", "same size company"
- **Conditions**: "missing JD", "no description", "with full JD"
- **Expectations**: "should match highly", "low match", "should conflict", "medium similarity"