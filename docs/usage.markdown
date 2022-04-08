---
# title: Use
---

## Use

1. [Finding nView Live](#finding-nview-live)
2. [Panel Settings](#panel-settings)
3. [How it runs](#running)

## Okay, I enabled nView Live, where is it? {#finding-nview-live}

1. Open the right toolbar for the the 3D viewport (the default shortcut is to press "T")
2. Click the "nView" tab

Here you will see the nView Live panel. If you do not, it may be an error.
Learn how you can report it [here](/contribute#report-bugs).

## Panel settings {#finding-nview-live}

- Maximum distance - any objects further than this distance from the camera will be
excluded from budget testing and automatically hidden.

### Budget subpanel
You can toggle budget prioritization as well as the following options:
- Budget type, which is locked while the modal is running.
  - "Object" - each object is given a cost of 1.
  - "Vertex" - cost equals the number of vertices belonging to the object.
  A single quad has a cost of 4.
  - "Triangle" - cost equals the number of triangles belonging to the object.
  A single quad has the cost of 2.
  This is the slowest of the budget calculations as it requires opening the mesh
  and calculating the triangles for each mesh.
- Budget limit - the maximum cost allowed in the viewport at any one time.
Once this limit is hit, all remaining objects will be hidden from view.
- Budget order (for vertex and triangle budgets) -
the order in which objects are prioritized:
ascending (lowest to highest cost) or descending (highest to lowest cost).

### Modal settings

Once you click the operator button, a modal window will appear with more settings:
- Delay - time in seconds to wait before running the visibility check after the viewport has updated.
- Object types - the types of objects to include in visibility tests:
  - meshes
  - instanced collections
  - lights

## Now it runs! What else do I need to do? {#running}

That's it! The addon will continue working as you navigate the scene
until you press the Escape key or right-click on the mouse.
You can use all the navigation-related commands, including FPS view, as well
as the animation playback.

Since this addon's main feature is exposed as a modal operator,
any other modal operation will cancel it
(such as using "G" to grab an object).
Otherwise, this modal will run in the background as you navigate your scene.