.. image:: _static/nview-live-logo.png


Official Documentation
=========================

This addon toggles an object's visibility in the viewport in realtime.
The main focus is to improve viewport performance in solid view.

Ideally, this addon could be converted into source code within Blender,
which would drastically improve this feature's performance and reliability.
Since it is relatively effective as an addon, I consider this a proof
of concept for the future and a useful tool for existing artists
with large, diverse scenes.

This addon supports Blender 3.0 and above (it may be compatible on older versions
but not guaranteed). This addon's functionality does _not_ guarantee
any performance ideal, such as an animation playback framerate.
In many cases, viewport performance is project-specific and requires scene management.
Neither does this addon bake visibility settings for renders or set render visibility.
For scene management and baking of visibility settings, see
my original `nView addon on Blender Market <https://blendermarket.com/products/nview>`_.

When the nView Live modal begins, it retrieves a list of objects in the scene.
Every time the active 3D viewport refreshes, the modal is triggered to
update visibility of all objects. The delay setting ensures the function
is only called once the viewport has stopped refreshing for a sufficient
amount of time, making it easier for users to navigate quickly and then
see updates once they've chosen a given view.
Using the caches, the callback checks which objects are visible.

If budgeting is enabled, it will track the objects currently visible
and the viewport cost. Any remaining objects are hidden.
The budget prioritizes objects closest to the viewport camera's location,
as well as the user's chosen budget priority.
If two objects have the same cost, the object closest to the camera is prioritized.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Download the add-on <https://github.com/semagnum/nview-live>

   use
   nview-live

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
