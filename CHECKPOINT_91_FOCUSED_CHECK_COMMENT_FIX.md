# CP91 Focused Check Comment Fix

This revision removes an obsolete script-name reference from the CP91 focused
check script. The check behavior is unchanged:

- all Chapter 1-related tests are collected explicitly,
- CP91 assembly tests are included,
- unrelated repository-wide tests are excluded,
- rollback remains enabled on any focused-test failure.
