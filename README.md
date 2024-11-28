# maya_timeline_bookmark_utils
A small, object oriented library to interact with as well as import / export Autodesk Maya's timeline bookmarks. 

## Import the library:
```python
import timelineBookmarks as tbm

# optionally reload it
from importlib import reload
reload(tbm)
```

## Examples:
Collect all bookmarks in the current scene and create the data objects
```python
bookmarks = tbm.get_maya_bookmarks()
```

Frame first bookmark
```python
bookmarks[0].frame()
```

Split and save Save the first two bookmarks as separate scene files
```python
tbm.split_bookmarks_to_scenes(bookmarks[:2], scene_name="Bookmark_Split", force=True)
```

## Import / Export 

Export bookmarks to file
```python
tbm.export_bookmarks(bookmarks)
```

Import bookmarks to file
```python
imported_bookmarks = tbm.import_bookmarks()
[bm.create_maya_node(update_existing=True) for bm in imported_bookmarks] # by default, nodes are not created automatically

imported_bookmarks = tbm.import_bookmarks(create_nodes=True, force_creation=True) # alternatively you can create on load - here we are force overriding existing nodes
```

