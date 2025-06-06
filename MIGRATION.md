# Migration Guide: Transitioning to External Validator

This document outlines the transition from embedded validator to the standalone models.validation repository.

## Phase 1: Current State (Embedded Validator)
- Validator lives in `/repository-validator/` within each repository
- Requires copying validator code to each repository
- Updates must be manually propagated

## Phase 2: Transition State (Dual Support)
- models.validation repository created and published
- Existing repositories continue using embedded validator
- New repositories use the GitHub Action

## Phase 3: Target State (External Validator)
- All repositories use `fcm-community/models.validation@v1`
- No embedded validator code needed
- Centralized updates and improvements

## Migration Steps

### For Repository Maintainers

1. **Update GitHub Workflow**
   ```yaml
   # Replace the entire validation job with:
   - name: Validate FCM compliance
     uses: fcm-community/models.validation@v1
     with:
       repository-type: 'framework'  # or auto-detect
       min-score: '0.8'
   ```

2. **Remove Embedded Validator**
   ```bash
   git rm -r repository-validator/
   git commit -m "chore: migrate to external FCM validator"
   ```

3. **Update Documentation**
   - Remove references to local validator
   - Point to models.validation repository

### For the models.validation Repository

1. **Publish to GitHub**
   - Create fcm-community/models.validation repository
   - Push all code from `/home/coder/project/models.validation/`
   - Create v1.0.0 release

2. **Enable GitHub Action**
   - Ensure action.yml is in repository root
   - Test with a sample repository

3. **Documentation**
   - Create comprehensive usage guide
   - Provide migration examples
   - Set up issue templates

## Benefits of Migration

- **Single Source of Truth**: One validator for all FCM repositories
- **Automatic Updates**: Improvements immediately available to all
- **Reduced Maintenance**: No need to copy/update validator code
- **Community Contributions**: Easier to contribute improvements
- **Follows FCM Principles**: Validator exists "beside" not "within"

## Timeline

- Week 1: Create and publish models.validation repository
- Week 2-3: Test with select repositories
- Week 4: Announce availability to community
- Week 5-8: Gradual migration of existing repositories
- Week 9+: Deprecate embedded validators