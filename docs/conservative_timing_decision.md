# Conservative Timing Decision

Auto1, Auto2, and Auto3 currently use conservative timing values that are
intentionally slower than the theoretical minimum.

This is an accepted reliability decision. Slow timing is safer than fast timing
because it gives FH6 menus, loading transitions, and user hardware more time to
respond consistently. Faster timing may work on one machine but fail on slower
systems, under momentary load, or when FH6 menu and loading behavior varies.

The current priority is reliability first. Auto1, Auto2, and Auto3 should favor
repeatable completion over maximum speed while the project is still validating
manual real-input behavior.

Auto3 specifically uses profile-driven keypress timings for menu navigation.
The current Auto3 timings are intentionally conservative after real-input menu
testing. They are working, but they are not optimized for speed.

F8 stop has been validated during Auto3 real-input testing. Timing optimization
does not change the stop-safety expectation: manual real-input paths must
remain interruptible and must preserve cleanup behavior.

Some current waits may be slower than necessary. That is not a silent issue or
bug; it is an explicitly accepted limitation until profile settings and profile
editing have been tested. Future timing optimization should remain
profile-driven so users can tune values for their own hardware without changing
automation code.

Auto3 timing optimization is postponed to final polish and profile tuning. This
is an explicitly accepted limitation, not a silent issue.
