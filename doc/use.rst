Usage
==========================================

Okay, I installed nView Live, where is it?
------------------------------------------

1. Open the right toolbar for the 3D view (the default shortcut is "n")
2. Click the "nView" tab

Here you will see the nView Live panel. If you do not, it may be due to an error.
You can report it `here <https://github.com/semagnum/nview-live/issues>`_.

Panel settings
==============

- **Delay** - time in seconds to wait before running the visibility check after the viewport has updated. For playback mode, this is the constant interval between each run of the visibility check.
- **Maximum distance** - any objects further than this distance from the camera will be excluded from budget testing and automatically hidden.
- **Show Hidden objects** - this button operator shows all hidden objects and acts as a reset button. This is the same operator as the one defaulted to the Alt-H keyboard shortcut.

Budget subpanel
----------------

You can toggle budget prioritization as well as the following options:

- **Budget type**, which is locked while the modal is running.

  - Object - an object's cost of 1.
  - Vertex - an object's cost equals the number of its vertices.  A single quad has a cost of 4.
  - Triangle - cost equals the number of triangles belonging to the object.  A single quad has the cost of 2. This is the slowest of the budget calculations as it requires evaluating each mesh.

- **Budget limit** - the maximum cost allowed in the viewport at any one time. Once this limit is hit, all remaining objects will be hidden from view.
- **Budget order** (for vertex and triangle budgets) - the order in which objects are prioritized: ascending (lowest to highest cost) or descending (highest to lowest cost).

Modal Settings
--------------

Once you click the operator button, a modal window will appear with more settings:

- **Minimum Bounding Box Size** - For objects without a determinable size (such as lights or non-instancing empties), they will be given a minimum bounding box of at least this size.
- **Playback mode** - Ideal mode for previewing animations. Instead of updating with a delay after viewport refresh, the modal refreshes at regular intervals (based on delay setting).
- **Exclude instanced objects** - objects within instanced collections are excluded from visibility tests (disabling this can result in instanced collections being partially hidden).
- **Object types** - the types of objects to include in visibility tests:

  - meshes
  - instanced collections
  - lights

Now it runs! What else do I need to do?
-----------------------------------------

That's it! The addon will continue working as you navigate the scene
until you press the Escape key or right-click on the mouse.
You can use all the navigation-related commands, including FPS view, as well
as the animation playback.

Since this addon's main feature is exposed as a modal operator,
any other modal operation will cancel it (such as using "G" to grab an object).
Otherwise, this modal will run in the background as you navigate your scene.