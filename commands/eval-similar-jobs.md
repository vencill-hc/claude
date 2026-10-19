# eval-similar-jobs

Run similar jobs evaluation tests to verify the similarity algorithm with real OpenAI API calls

## Arguments (optional)
- Test name: Run a specific test case by name
- Example: `/eval-similar-jobs "Same role, different seniority levels"`

## Steps I will take:
1. Check if test file exists at `config/similar_jobs_eval.yml`
2. Run the evaluation using rails runner:
   - If no argument: `rails runner "load 'lib/tasks/similar_jobs_eval.rake'; SimilarJobsEval.new.run"`
   - If test name provided: `rails runner "load 'lib/tasks/similar_jobs_eval.rake'; SimilarJobsEval.new.run(test_name: 'TEST_NAME')"`
3. Display the colored output showing:
   - Each test case with source and target jobs
   - Actual similarity scores vs expected ranges
   - Match reasons validation
   - Pass/fail status for each test
4. Show summary statistics at the end
5. Clean up all test projects automatically

## What this does:
- Creates temporary projects with specific attributes
- Generates real embeddings using OpenAI's text-embedding-3-small model
- Calls SimilarProjectsService with LLM re-ranking (GPT-5-mini)
- Compares actual results against expected scores
- Validates the similar jobs algorithm is working correctly

## Example usage:
```
/eval-similar-jobs
/eval-similar-jobs "Remote vs onsite conflict"
```