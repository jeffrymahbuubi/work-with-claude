---
name: example-skill
category: dev
description: Template skill demonstrating how to create reusable workflows with clear steps and validation
usage: Use when you need a template for creating custom skills or want to understand skill structure
input: Task requirements, workflow steps to automate
output: A structured, repeatable workflow with validation checkpoints
---

# Example Skill - Template for Creating Custom Skills

## Overview

**Purpose**: Demonstrate the structure and best practices for creating custom skills in Claude Code

**Category**: Development
**Primary Users**: Developers creating reusable workflows

This skill serves as a template showing how to create structured, repeatable workflows with:
- Clear step-by-step processes
- Validation checkpoints
- Expected inputs and outputs
- Best practices and common patterns

## When to Use This Skill

Use this template when creating skills for:

- Multi-step technical workflows (build, test, deploy)
- Data processing pipelines
- Code generation workflows
- Documentation generation
- Analysis and reporting tasks
- Quality assurance processes
- Any repeatable multi-step task

## Prerequisites

**Required:**
- Understanding of the workflow you want to automate
- Knowledge of tools and commands needed
- Clear definition of inputs and expected outputs

**Optional:**
- Example inputs for testing
- Documentation of edge cases
- Success criteria metrics

## Input

**What the skill needs:**
- Clear task description
- Required parameters or configuration
- Input data or files
- Environment variables or settings

**Example inputs:**
```json
{
  "workflow_name": "example-workflow",
  "input_files": ["file1.txt", "file2.txt"],
  "options": {
    "verbose": true,
    "output_format": "json"
  }
}
```

## Workflow

### Step 1: Initialize and Validate

**Objective**: Verify prerequisites and setup environment

**Actions:**
1. Check that required tools are available
2. Validate input parameters
3. Verify required files exist
4. Setup working directory

**Example:**
```bash
# Check for required tools
command -v python >/dev/null 2>&1 || { echo "Python required"; exit 1; }

# Validate input files
for file in "$@"; do
  [[ -f "$file" ]] || { echo "File not found: $file"; exit 1; }
done
```

**Validation:**
- [ ] All required tools available
- [ ] Input parameters valid
- [ ] Required files accessible
- [ ] Environment properly configured

**Output**: Validated environment ready for processing

---

### Step 2: Process Data

**Objective**: Execute main workflow logic

**Actions:**
1. Load and parse input data
2. Apply transformations
3. Execute core processing
4. Handle errors gracefully

**Example:**
```python
def process_data(input_file):
    try:
        # Load data
        with open(input_file, 'r') as f:
            data = f.read()

        # Transform
        result = transform(data)

        # Process
        output = process(result)

        return output
    except Exception as e:
        log_error(f"Processing failed: {e}")
        raise
```

**Validation:**
- [ ] Input data loaded successfully
- [ ] Transformations applied correctly
- [ ] Processing completed without errors
- [ ] Output data structure valid

**Output**: Processed data ready for next step

---

### Step 3: Generate Output

**Objective**: Format and save results

**Actions:**
1. Format output according to requirements
2. Validate output structure
3. Write to destination
4. Generate summary/report

**Example:**
```python
def generate_output(data, output_file, format='json'):
    if format == 'json':
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
    elif format == 'csv':
        pd.DataFrame(data).to_csv(output_file)

    print(f"Output written to {output_file}")
    return output_file
```

**Validation:**
- [ ] Output formatted correctly
- [ ] File written successfully
- [ ] Output readable and valid
- [ ] Summary generated

**Output**: Final output file and summary report

---

### Step 4: Verify and Report

**Objective**: Confirm success and provide feedback

**Actions:**
1. Verify output integrity
2. Run validation checks
3. Generate detailed report
4. Provide next steps

**Example:**
```python
def verify_output(output_file):
    # Check file exists and is not empty
    assert os.path.exists(output_file), "Output file missing"
    assert os.path.getsize(output_file) > 0, "Output file empty"

    # Validate content
    with open(output_file, 'r') as f:
        data = json.load(f)

    # Generate report
    report = {
        "status": "success",
        "output_file": output_file,
        "record_count": len(data),
        "timestamp": datetime.now().isoformat()
    }

    return report
```

**Validation:**
- [ ] Output file integrity confirmed
- [ ] Validation checks passed
- [ ] Report generated
- [ ] Next steps documented

**Output**: Verification report and completion status

---

## Output

**Produces:**
- Processed output files
- Validation reports
- Execution summary
- Logs and diagnostics

**Success Criteria:**
- All validation checkpoints passed
- Output meets specifications
- No critical errors occurred
- Documentation generated

**Example output:**
```json
{
  "status": "success",
  "workflow": "example-skill",
  "input_files": ["file1.txt", "file2.txt"],
  "output_file": "output.json",
  "records_processed": 1543,
  "duration_seconds": 2.3,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Best Practices

### Workflow Design

1. **Break into logical steps**: Each step should do one clear thing
2. **Validate at checkpoints**: Catch errors early
3. **Make steps independent**: Each step should be self-contained
4. **Document assumptions**: Be explicit about requirements
5. **Provide examples**: Show concrete inputs and outputs

### Error Handling

1. **Fail fast**: Validate inputs before processing
2. **Clear error messages**: Explain what went wrong and how to fix it
3. **Graceful degradation**: Have fallback options when possible
4. **Log everything**: Make debugging easier

### Code Quality

1. **Keep it simple**: Don't overcomplicate
2. **Make it reusable**: Parameterize what might change
3. **Test thoroughly**: Verify with different inputs
4. **Document well**: Future you will thank you

### User Experience

1. **Show progress**: Let users know what's happening
2. **Provide feedback**: Confirm successful completion
3. **Suggest next steps**: Guide users forward
4. **Make it discoverable**: Clear description and usage

## Common Patterns

### File Processing Pipeline

```yaml
1. Validate file exists
2. Read and parse file
3. Transform data
4. Validate transformed data
5. Write output
6. Verify output integrity
```

### API Integration Workflow

```yaml
1. Load credentials from environment
2. Authenticate with API
3. Fetch data from endpoints
4. Process and transform
5. Save locally
6. Generate report
```

### Build and Test Pipeline

```yaml
1. Clean previous builds
2. Install dependencies
3. Run linters
4. Execute tests
5. Generate coverage report
6. Build artifacts
```

## Creating Your Own Skill

### 1. Choose a Skill Name

- Use kebab-case (lowercase with hyphens)
- Make it descriptive and specific
- Keep it short (2-3 words)

### 2. Define the Workflow

Break your process into 3-6 main steps:
- Each step should have a clear objective
- List specific actions for each step
- Define validation criteria
- Specify expected outputs

### 3. Write the SKILL.md

Use this template structure:
- Frontmatter with metadata
- Overview section
- When to Use section
- Prerequisites
- Input specification
- Workflow (steps)
- Output specification
- Best Practices
- Common Patterns

### 4. Test Your Skill

- Test with various inputs
- Verify validation catches errors
- Ensure output is correct
- Check error messages are helpful

### 5. Document Edge Cases

- What happens with empty input?
- How are errors handled?
- What are the limitations?
- Any special requirements?

## Example: Creating a Test Runner Skill

```markdown
---
name: test-runner
category: dev
description: Run project tests with coverage reporting
usage: Use when you need to run tests and generate coverage reports
input: Test directory path, coverage threshold
output: Test results and coverage report
---

# Test Runner Skill

## Workflow

### Step 1: Setup Test Environment
- Activate virtual environment
- Install test dependencies
- Clean previous test artifacts

### Step 2: Run Tests
- Execute test suite
- Capture output
- Handle test failures

### Step 3: Generate Coverage Report
- Run coverage analysis
- Generate HTML report
- Check coverage threshold

### Step 4: Report Results
- Display test summary
- Show coverage percentage
- Provide links to reports
```

## Notes

- Skills are invoked with `/skill-name` in conversation
- Skills should be self-contained workflows
- Each step should have clear validation
- Provide helpful error messages
- Document all prerequisites
- Include usage examples
- Keep workflows focused and simple

## Skill Frontmatter Reference

### Required Fields
- `name`: Skill identifier (kebab-case)
- `description`: What this skill does
- `usage`: When to use this skill
- `input`: What inputs are needed
- `output`: What outputs are produced

### Optional Fields
- `category`: Skill category (dev, docs, data, etc.)
- `prerequisites`: Required tools or setup
- `examples`: Usage examples

---

**This is a template. Customize for your actual workflow.**
