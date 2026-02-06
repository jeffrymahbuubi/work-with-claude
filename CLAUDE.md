# CLAUDE.md

This file provides project-specific guidance to Claude Code when working with code in this repository.

## Project Overview

[Describe your project here - what it does, its purpose, key technologies]

**Example:**
```
This is a [web app/library/tool] that [brief description of purpose].
Built with [main technologies].
```

## Environment & Setup

### Running the Project

[Document how to run the project]

**Example:**
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Environment Variables

[List required environment variables]

**Example:**
```
Required:
- DATABASE_URL: PostgreSQL connection string
- API_KEY: Third-party API key

Optional:
- DEBUG: Enable debug mode (default: false)
- PORT: Server port (default: 3000)
```

### Dependencies

[Document dependency management]

**Example:**
```
Dependencies are managed with [npm/pip/cargo/etc].
Always use [package manager] to install packages.
Lock file: [package-lock.json/requirements.txt/Cargo.lock]
```

## Repository Structure

```
[Document your project structure]

Example:
src/
├── components/          # React components
├── lib/                 # Utility functions
├── services/            # API services
└── types/              # TypeScript types

tests/                   # Test files
docs/                    # Documentation
scripts/                 # Build and utility scripts
```

## Development Guidelines

### Code Style

[Document coding standards and style guidelines]

**Example:**
```
- Use TypeScript for all new code
- Follow Airbnb style guide
- Run `npm run lint` before committing
- Use meaningful variable names
- Add comments for complex logic
```

### Testing

[Document testing practices]

**Example:**
```
- Write tests for all new features
- Aim for >80% coverage
- Test file naming: `[name].test.ts`
- Run tests: `npm test`
- Run coverage: `npm run test:coverage`
```

### Git Workflow

[Document your git workflow]

**Example:**
```
- Create feature branches from `main`
- Branch naming: `feature/description` or `fix/description`
- Commit message format: `[type]: description`
  - Types: feat, fix, docs, style, refactor, test, chore
- Open PR when ready for review
- Squash merge to main
```

## Important Conventions

### Naming Conventions

[Document naming patterns]

**Example:**
```
- Components: PascalCase (UserProfile.tsx)
- Functions: camelCase (getUserData)
- Constants: UPPER_SNAKE_CASE (API_BASE_URL)
- Files: kebab-case (user-profile.ts)
```

### File Organization

[Document how files should be organized]

**Example:**
```
- One component per file
- Co-locate tests with source files
- Group related files in directories
- Index files for clean imports
```

## Scripts and Commands

### Available Scripts

[Document available npm/make/etc scripts]

**Example:**
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run test suite
npm run lint         # Run linter
npm run format       # Format code
npm run typecheck    # Run TypeScript checks
```

### Custom Scripts

[Document any custom scripts in your scripts/ directory]

**Example:**
```bash
./scripts/claude-with-env.sh  # Launch Claude with .env loaded
./scripts/deploy.sh          # Deploy to production
./scripts/seed-db.sh         # Seed database with test data
```

## API Documentation

[Document API structure if applicable]

**Example:**
```
API Base URL: /api/v1

Endpoints:
- GET /api/v1/users        # List users
- POST /api/v1/users       # Create user
- GET /api/v1/users/:id    # Get user
- PUT /api/v1/users/:id    # Update user
- DELETE /api/v1/users/:id # Delete user

Authentication: Bearer token in Authorization header
```

## Database

[Document database schema and migrations]

**Example:**
```
Database: PostgreSQL 14+
ORM: Prisma

Run migrations: npx prisma migrate dev
View database: npx prisma studio
Reset database: npx prisma migrate reset
```

## Common Tasks

### Adding a New Feature

[Step-by-step guide for common tasks]

**Example:**
```
1. Create feature branch
2. Add types in src/types/
3. Implement feature in src/
4. Write tests in tests/
5. Update documentation
6. Run linter and tests
7. Open PR
```

### Debugging

[Document debugging practices]

**Example:**
```
- Use console.log() for quick debugging
- Use debugger; for breakpoints
- Check logs: npm run logs
- Inspect database: npx prisma studio
- Enable debug mode: DEBUG=* npm run dev
```

## Known Issues & Gotchas

[Document any quirks or known issues]

**Example:**
```
- Issue: Hot reload sometimes fails
  Fix: Restart dev server

- Issue: Tests fail with ECONNREFUSED
  Fix: Ensure test database is running

- Gotcha: API rate limit is 100 req/min
  Note: Implement request throttling
```

## Dependencies and Packages

[Document important dependencies]

**Example:**
```
Core:
- React 18 - UI framework
- TypeScript 5 - Type safety
- Vite - Build tool

Key libraries:
- zod - Runtime validation
- tanstack-query - Data fetching
- zustand - State management
```

## Deployment

[Document deployment process]

**Example:**
```
Production: https://example.com
Staging: https://staging.example.com

Deploy to staging: npm run deploy:staging
Deploy to production: npm run deploy:prod

CI/CD: GitHub Actions on push to main
```

## Resources

[Link to relevant documentation]

**Example:**
```
- Project Wiki: [URL]
- API Docs: [URL]
- Design System: [URL]
- Team Guidelines: [URL]
```

## Contact & Support

[Document how to get help]

**Example:**
```
- Tech Lead: @username
- Slack Channel: #project-name
- Issue Tracker: GitHub Issues
- Documentation: /docs
```

---

## Notes for Claude

[Specific instructions for Claude Code]

**Example guidelines:**
```
When working on this project:

1. Always run tests before committing
2. Follow TypeScript best practices
3. Use existing patterns for consistency
4. Ask before making breaking changes
5. Update documentation with code changes
6. Use project's ESLint/Prettier config
7. Prefer composition over inheritance
8. Keep components small and focused
9. Write meaningful commit messages
10. Document complex logic

Don't:
- Don't use 'any' type without good reason
- Don't commit directly to main
- Don't skip tests
- Don't ignore linter warnings
- Don't hard-code configuration
```

---

**Customize this template for your specific project!**

Remove placeholder sections and add project-specific information.
