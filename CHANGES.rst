=======
Changes
=======

0.5.0 / 2019-14-04
==================
* Add new methods `StatusMap.get_ancestors()` and `StatusMap.get_descendants()` to calculate and cache paths to avoid recalculate them every time

0.4.0 / 2019-12-04
==================
* Add Error suffix to exceptions names
* Add AmbiguousTransitionError when the map has a cycle and the status transition can be both past and future
* Use networkx and graph internally


0.3.0 / 2019-06-04
==================

* Add custom representation for StatusMap
* Improve StatusNotFound exception message
* Add StatusMap.statuses property
* Disable "previous" list of status when StatusMap is cycle, otherwise the previous status are added

0.2.0 / 2019-06-04
==================

* Fix StatusMap processing to always procude the same results

0.1.0 / 2019-06-03
==================

* Initial release
* Add StatusMap (and Status) with status validation support
